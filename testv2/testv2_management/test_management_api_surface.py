"""
Discovery-based regression covering every generated Management API operation.

For each primary method on every *Api class:
1. Call the generated _*_serialize helper with placeholder args
2. Assert a valid HTTP method + /api/ path are produced
3. Assert ManagementClient exposes the owning API attribute

This catches regen drift (dropped/renamed operations, broken path templates,
broken snake_case exposure) across the full ~178-operation surface without
hand-writing one test per endpoint.
"""

from __future__ import annotations

import inspect
from typing import Any, Dict, List, Optional, Tuple, Union, get_args, get_origin

import pytest
from pydantic import BaseModel

from kinde_sdk.management import api as management_api
from kinde_sdk.management.api_client import ApiClient
from kinde_sdk.management.configuration import Configuration
from kinde_sdk.management.management_client import ManagementClient

from .helpers import DOMAIN, build_management_client


def _unwrap_optional(annotation: Any) -> Any:
    origin = get_origin(annotation)
    if origin is Union:
        args = [arg for arg in get_args(annotation) if arg is not type(None)]
        return args[0] if len(args) == 1 else annotation
    return annotation


def _is_bytes_like(annotation: Any) -> bool:
    annotation = _unwrap_optional(annotation)
    if annotation in (bytes, bytearray):
        return True
    origin = get_origin(annotation)
    if origin is Union:
        return any(
            arg in (bytes, bytearray) or get_origin(arg) is tuple
            for arg in get_args(annotation)
        )
    return False


def _make_placeholder(name: str, annotation: Any) -> Any:
    """Build a value good enough to exercise param_serialize for regression."""
    if name in ("logo",) or _is_bytes_like(annotation):
        # File upload params accept raw bytes; strings are treated as paths.
        return b"fake-logo-bytes"

    annotation = _unwrap_optional(annotation)
    origin = get_origin(annotation)

    if annotation is inspect.Parameter.empty:
        if name.endswith("_request") or name.endswith("request"):
            return {"_test_placeholder": True}
        if name.endswith("_size") or name in ("page_size",):
            return 10
        if name.startswith("include_") or name.startswith("is_"):
            return True
        return f"test_{name}"

    if annotation is str:
        if name == "type":
            return "dark"
        return f"test_{name}"
    if annotation is int:
        return 10
    if annotation is bool:
        return True
    if annotation in (bytes, bytearray):
        return b"fake-bytes"
    if origin in (list, List):
        return []
    if origin in (dict, Dict):
        return {}
    if origin is tuple:
        return ("logo.png", b"fake-logo-bytes")

    if inspect.isclass(annotation) and issubclass(annotation, BaseModel):
        try:
            return annotation()
        except Exception:
            # Construct with required string placeholders; enums may still fail
            # and fall through to a plain dict that param_serialize accepts.
            required = {
                field_name: f"test_{field_name}"
                for field_name, field in annotation.model_fields.items()
                if field.is_required()
            }
            try:
                return annotation.model_construct(**required)
            except Exception:
                return required

    return f"test_{name}"


def _discover_operations() -> List[Tuple[str, str]]:
    ops: List[Tuple[str, str]] = []
    for class_name, cls in inspect.getmembers(management_api):
        if not (inspect.isclass(cls) and class_name.endswith("Api")):
            continue
        for method_name, _method in inspect.getmembers(cls, predicate=inspect.isfunction):
            if method_name.startswith("_"):
                continue
            if method_name.endswith("_with_http_info"):
                continue
            if method_name.endswith("_without_preload_content"):
                continue
            ops.append((class_name, method_name))
    return sorted(ops)


ALL_OPERATIONS = _discover_operations()


@pytest.fixture(scope="module")
def api_client() -> ApiClient:
    return ApiClient(configuration=Configuration(host=f"https://{DOMAIN}"))


@pytest.fixture(scope="module")
def management_client() -> ManagementClient:
    return build_management_client()


def test_discovered_operation_count_is_stable():
    """Guardrail: unexpected large drops/gains in generated surface."""
    assert len(ALL_OPERATIONS) >= 170, (
        f"Expected ~178 management operations, found {len(ALL_OPERATIONS)}"
    )


@pytest.mark.parametrize("class_name,method_name", ALL_OPERATIONS)
def test_operation_serializes_valid_request(
    api_client: ApiClient, class_name: str, method_name: str
):
    cls = getattr(management_api, class_name)
    instance = cls(api_client=api_client)
    serialize = getattr(instance, f"_{method_name}_serialize")

    kwargs: Dict[str, Any] = {}
    for param_name, param in inspect.signature(serialize).parameters.items():
        if param_name == "self":
            continue
        if param_name.startswith("_"):
            kwargs[param_name] = 0 if param_name == "_host_index" else None
        else:
            kwargs[param_name] = _make_placeholder(param_name, param.annotation)

    method, url, headers, _body, *_rest = serialize(**kwargs)

    assert method in {"GET", "POST", "PUT", "PATCH", "DELETE"}
    assert "/api/" in url, f"{class_name}.{method_name} URL missing /api/: {url}"
    assert isinstance(headers, dict)
    assert "Accept" in headers or method == "DELETE"


@pytest.mark.parametrize("class_name,method_name", ALL_OPERATIONS)
def test_operation_exposed_on_management_client(
    management_client: ManagementClient, class_name: str, method_name: str
):
    attr_name = ManagementClient._class_name_to_snake_case(class_name)
    assert hasattr(management_client, attr_name), (
        f"ManagementClient missing {attr_name} for {class_name}"
    )
    api_instance = getattr(management_client, attr_name)
    assert hasattr(api_instance, method_name), (
        f"client.{attr_name} missing method {method_name}"
    )
    assert callable(getattr(api_instance, method_name))


def test_all_api_classes_have_unique_client_attributes(management_client: ManagementClient):
    class_names = [
        name
        for name, obj in inspect.getmembers(management_api)
        if inspect.isclass(obj) and name.endswith("Api")
    ]
    attrs = [ManagementClient._class_name_to_snake_case(name) for name in class_names]
    assert len(attrs) == len(set(attrs)), "Duplicate snake_case API attribute names"
    for attr in attrs:
        assert attr.endswith("_api")
        assert attr.islower()
        assert "__" not in attr
        assert getattr(management_client, attr).api_client is management_client.api_client
