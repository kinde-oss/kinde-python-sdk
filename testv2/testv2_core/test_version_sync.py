"""Regression tests guarding the single source of truth for the SDK version.

``kinde_sdk/_version.py`` is the only place the SDK version should be
edited (see PR #182). Everything else derives from it:

* the top-level ``kinde_sdk`` package re-exports it;
* the generated ``kinde_sdk.frontend`` and ``kinde_sdk.management``
  sub-packages re-export it via a post-generation rewrite;
* the distribution metadata produced from ``pyproject.toml`` resolves
  from it dynamically.

The two OpenAPI generator configs (``openapitools.json`` for management,
``generator/frontend_config.yaml`` for frontend) use a different
discipline: they both store the literal self-documenting placeholder
``"SDK_VERSION"`` in their ``packageVersion`` field, and the resolved
value is injected at runtime via
``--additional-properties=packageVersion=<SDK_VERSION>`` on the
``openapi-generator-cli`` command line. This makes it visually
impossible for either file to be mistaken for a second source of truth,
and the tests below assert the placeholder invariant.

These tests fail loudly the moment any of those surfaces gets out of
sync (or a placeholder regresses to a literal), so a future release
can't silently reintroduce the drift PR #182 was written to eliminate.
"""

import json
from importlib.metadata import PackageNotFoundError, version as dist_version
from pathlib import Path

import pytest

import kinde_sdk
import kinde_sdk.frontend
import kinde_sdk.management
from kinde_sdk._version import __version__ as sot_version

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_top_level_package_version_matches_source_of_truth():
    assert kinde_sdk.__version__ == sot_version


def test_frontend_subpackage_version_matches_source_of_truth():
    assert kinde_sdk.frontend.__version__ == sot_version


def test_management_subpackage_version_matches_source_of_truth():
    assert kinde_sdk.management.__version__ == sot_version


def test_distribution_metadata_matches_source_of_truth():
    """pyproject.toml resolves its version dynamically from ``kinde_sdk._version``.

    When the package is installed (editable or otherwise) the installed
    dist metadata - which is what ``SDKTracker`` reads to build the
    User-Agent header sent to Kinde - must match the source-of-truth
    string. We skip when the package isn't installed (e.g. raw checkout
    without ``pip install -e .``), since there is no metadata to check
    in that case.
    """
    try:
        installed = dist_version("kinde-python-sdk")
    except PackageNotFoundError:
        pytest.skip("kinde-python-sdk is not installed; nothing to compare against")

    assert installed == sot_version


OPENAPITOOLS_PACKAGE_VERSION_PLACEHOLDER = "SDK_VERSION"
FRONTEND_CONFIG_PACKAGE_VERSION_PLACEHOLDER = "SDK_VERSION"


def test_openapitools_json_package_version_is_self_documenting_placeholder():
    """``openapitools.json``'s ``packageVersion`` must be the placeholder, not a literal.

    The committed ``openapitools.json`` is deliberately *not* a version
    literal - it stores the self-documenting placeholder
    ``"SDK_VERSION"`` (same name as the Python constant in
    ``generate_management_sdk.py`` that holds the resolved value). This
    makes it impossible to mistake the file for a second source of truth.

    The resolved version is injected at runtime via
    ``--additional-properties=packageVersion=<SDK_VERSION>`` on the
    ``openapi-generator-cli`` command line, which overrides the file's
    placeholder. As an additional safety net,
    ``generate_management_sdk.py::make_version_dynamic`` rewrites the
    generator-emitted ``__version__`` line in the produced ``__init__.py``
    to import from ``kinde_sdk._version``, so the placeholder never
    reaches a wrapper-generated artifact.

    This test fails if anyone (a) reintroduces a version literal into the
    file or (b) replaces the placeholder with a different sentinel
    without also updating ``ensure_openapitools_config``.
    """
    config_path = REPO_ROOT / "openapitools.json"
    assert config_path.exists(), (
        f"Expected {config_path} to exist; the management generator config "
        "is part of the version SSoT chain."
    )

    with config_path.open(encoding="utf-8") as f:
        openapitools_config = json.load(f)

    try:
        package_version = (
            openapitools_config["generator-cli"]["generators"]["management"]
            ["additionalProperties"]["packageVersion"]
        )
    except KeyError as exc:
        pytest.fail(
            f"openapitools.json is missing the expected "
            f"generator-cli.generators.management.additionalProperties.packageVersion "
            f"path: {exc}. Did the file's schema change? Update "
            "generate_management_sdk.py::ensure_openapitools_config and this test."
        )

    assert package_version == OPENAPITOOLS_PACKAGE_VERSION_PLACEHOLDER, (
        f"openapitools.json packageVersion is {package_version!r}, expected "
        f"the self-documenting placeholder "
        f"{OPENAPITOOLS_PACKAGE_VERSION_PLACEHOLDER!r}. The committed file must "
        "not hold a version literal - that would make it a second source of "
        "truth that could drift from kinde_sdk/_version.py. Run "
        "`python3 generate_management_sdk.py` to reset the placeholder. The "
        f"resolved version ({sot_version}) is supplied at runtime via "
        "--additional-properties on the openapi-generator-cli command line; see "
        "generate_management_sdk.py::ensure_openapitools_config."
    )


def test_frontend_generator_config_package_version_is_self_documenting_placeholder():
    """``generator/frontend_config.yaml``'s ``packageVersion`` must be the placeholder.

    ``generate_frontend_sdk.py`` rewrites this file from a template literal
    on every run, holding the self-documenting placeholder
    ``"SDK_VERSION"`` (same string as the Python constant
    ``FRONTEND_CONFIG_PACKAGE_VERSION_PLACEHOLDER`` in that script). The
    resolved version is injected at runtime via
    ``--additional-properties=packageVersion=<SDK_VERSION>`` on the
    ``openapi-generator-cli`` command line, which overrides the YAML
    placeholder. As an additional safety net, ``make_version_dynamic``
    rewrites the generator-emitted ``__version__`` line in the produced
    ``__init__.py`` to import from ``kinde_sdk._version`` so the
    placeholder never reaches a wrapper-generated artifact.

    The YAML file is not tracked in git; it's a transient artifact written
    by the wrapper. When the file is present in the checkout (i.e. the
    script has been run) this test asserts the placeholder invariant. If
    the file is absent, the test skips. This mirrors the management
    generator's ``openapitools.json`` treatment for end-to-end symmetry.
    """
    config_path = REPO_ROOT / "generator" / "frontend_config.yaml"
    if not config_path.exists():
        pytest.skip(
            "generator/frontend_config.yaml has not been written yet "
            "(generate_frontend_sdk.py has not been run in this checkout)"
        )

    package_version = None
    for line in config_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("packageVersion:"):
            package_version = stripped.split(":", 1)[1].strip().strip('"').strip("'")
            break

    assert package_version is not None, (
        f"Could not find a `packageVersion:` line in {config_path}; "
        "did generate_frontend_sdk.py's template change?"
    )
    assert package_version == FRONTEND_CONFIG_PACKAGE_VERSION_PLACEHOLDER, (
        f"{config_path} packageVersion is {package_version!r}, expected "
        f"the self-documenting placeholder "
        f"{FRONTEND_CONFIG_PACKAGE_VERSION_PLACEHOLDER!r}. The YAML must not "
        "hold a version literal - that would make it a second source of truth "
        f"that could drift from kinde_sdk/_version.py. Run "
        "`python3 generate_frontend_sdk.py` to reset the placeholder. The "
        f"resolved version ({sot_version}) is supplied at runtime via "
        "--additional-properties on the openapi-generator-cli command line; "
        "see generate_frontend_sdk.py."
    )
