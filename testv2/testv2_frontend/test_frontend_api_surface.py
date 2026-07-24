"""
Discovery-based smoke/regression for the generated Frontend (Account) API.

Mirrors the management surface suite: every primary operation must serialize
to a valid HTTP request so frontend regenerations don't silently drop methods.
"""

from __future__ import annotations

import inspect
from typing import Any, Dict, List, Tuple, Union, get_args, get_origin

import pytest
from pydantic import BaseModel

from kinde_sdk.frontend import api as frontend_api
from kinde_sdk.frontend.api_client import ApiClient
from kinde_sdk.frontend.configuration import Configuration


def _unwrap_optional(annotation: Any) -> Any:
    origin = get_origin(annotation)
    if origin is Union:
        args = [arg for arg in get_args(annotation) if arg is not type(None)]
        return args[0] if len(args) == 1 else annotation
    return annotation


def _make_placeholder(name: str, annotation: Any) -> Any:
    annotation = _unwrap_optional(annotation)
    origin = get_origin(annotation)

    if annotation is inspect.Parameter.empty:
        if name.endswith("_request") or "request" in name:
            return {"_test_placeholder": True}
        if name.endswith("_size") or name == "page_size":
            return 10
        return f"test_{name}"

    if annotation is str:
        return f"test_{name}"
    if annotation is int:
        return 10
    if annotation is bool:
        return True
    if origin in (list, List):
        return []
    if origin in (dict, Dict):
        return {}
    if inspect.isclass(annotation) and issubclass(annotation, BaseModel):
        try:
            return annotation()
        except Exception:
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
    for class_name, cls in inspect.getmembers(frontend_api):
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
    return ApiClient(configuration=Configuration(host="https://test.kinde.com"))


def test_frontend_api_classes_are_exported():
    expected = {
        "BillingApi",
        "FeatureFlagsApi",
        "OAuthApi",
        "PermissionsApi",
        "PropertiesApi",
        "RolesApi",
        "SelfServePortalApi",
    }
    discovered = {
        name
        for name, obj in inspect.getmembers(frontend_api)
        if inspect.isclass(obj) and name.endswith("Api")
    }
    assert expected == discovered


def test_discovered_frontend_operation_count():
    assert len(ALL_OPERATIONS) >= 8
    assert len(ALL_OPERATIONS) <= 50


@pytest.mark.parametrize("class_name,method_name", ALL_OPERATIONS)
def test_frontend_operation_serializes_valid_request(
    api_client: ApiClient, class_name: str, method_name: str
):
    cls = getattr(frontend_api, class_name)
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
    assert isinstance(url, str) and len(url) > 0
    assert isinstance(headers, dict)
