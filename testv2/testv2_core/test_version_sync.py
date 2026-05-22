"""Regression tests guarding the single source of truth for the SDK version.

``kinde_sdk/_version.py`` is the only place the SDK version should be
edited (see PR #182). Everything else - the top-level ``kinde_sdk``
package, the generated ``kinde_sdk.frontend`` and ``kinde_sdk.management``
sub-packages, and the distribution metadata produced from
``pyproject.toml`` - must derive from it.

These tests fail loudly the moment any of those gets out of sync, so a
future release can't silently reintroduce the drift PR #182 was written
to eliminate.
"""

from importlib.metadata import PackageNotFoundError, version as dist_version

import pytest

import kinde_sdk
import kinde_sdk.frontend
import kinde_sdk.management
from kinde_sdk._version import __version__ as sot_version


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
