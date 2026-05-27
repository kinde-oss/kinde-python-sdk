"""Shared helpers for the OpenAPI generator wrapper scripts.

Both ``generate_management_sdk.py`` and ``generate_frontend_sdk.py`` need
to do the same handful of version-related operations: resolve the SDK
version from ``kinde_sdk/_version.py``, know the
``"SDK_VERSION"`` placeholder used in the generator config files, and
post-process the OpenAPI-emitted ``__init__.py`` so its ``__version__``
is imported from ``kinde_sdk._version`` rather than baked in as a
literal. Keeping a single implementation of each here eliminates the
slow drift that was starting to appear between the two scripts (e.g.
diverging type annotations, log message styling, and error handling).

The module is intentionally named with a leading underscore to signal
that it is internal to this repository's generator tooling; it is not
part of the public ``kinde_sdk`` package and is not shipped as part of
the distribution.
"""

from __future__ import annotations

import re
from pathlib import Path


# ---------------------------------------------------------------------------
# Version resolution
# ---------------------------------------------------------------------------

# Path to the single source of truth for the SDK version. Both generator
# scripts sit at the repo root next to ``kinde_sdk/``, and so does this
# module - so ``Path(__file__).resolve().parent`` is the repo root.
_VERSION_FILE = Path(__file__).resolve().parent / "kinde_sdk" / "_version.py"


def read_sdk_version() -> str:
    """Read the canonical SDK version string from ``kinde_sdk/_version.py``.

    The resolved value is supplied to ``openapi-generator-cli`` at
    runtime via ``--additional-properties=packageVersion=<SDK_VERSION>``
    so that artifacts which embed the version literally (e.g. user-agent
    headers in the generated ``configuration.py``) stay in lockstep with
    the SDK. The generator config files themselves
    (``openapitools.json`` and ``generator/frontend_config.yaml``)
    hold the literal placeholder :data:`PACKAGE_VERSION_PLACEHOLDER` so
    they cannot become second sources of truth; see
    ``testv2/testv2_core/test_version_sync.py`` for the enforcing tests.

    Raises:
        RuntimeError: if ``_version.py`` exists but no ``__version__``
            assignment can be parsed out of it.
    """
    text = _VERSION_FILE.read_text(encoding="utf-8")
    match = re.search(
        r'^__version__\s*=\s*["\']([^"\']+)["\']', text, re.MULTILINE
    )
    if not match:
        raise RuntimeError(
            f"Could not parse __version__ from {_VERSION_FILE}; "
            "the generator can't derive packageVersion."
        )
    return match.group(1)


#: Resolved SDK version, ready for both generator scripts to use.
SDK_VERSION: str = read_sdk_version()


# ---------------------------------------------------------------------------
# Generator-config placeholder
# ---------------------------------------------------------------------------

#: Literal string written into the ``packageVersion`` field of both
#: generator config files (``openapitools.json`` and
#: ``generator/frontend_config.yaml``). The committed/written value is
#: deliberately *not* a version literal - it is this self-documenting
#: placeholder, so the files cannot be mistaken for a second source of
#: truth. The resolved version is injected at runtime via
#: ``--additional-properties=packageVersion=<SDK_VERSION>`` on the
#: ``openapi-generator-cli`` command line, which overrides whatever the
#: file contains. The placeholder invariant is asserted in CI by
#: ``testv2/testv2_core/test_version_sync.py``.
PACKAGE_VERSION_PLACEHOLDER: str = "SDK_VERSION"


# ---------------------------------------------------------------------------
# Post-generation ``__version__`` rewrite
# ---------------------------------------------------------------------------

#: Line written into the generated sub-package ``__init__.py`` in place
#: of the OpenAPI-emitted ``__version__ = "..."`` literal. Holding a
#: single constant here means both generator scripts (and any future
#: ones) emit byte-identical replacements.
DYNAMIC_VERSION_IMPORT: str = (
    "from kinde_sdk._version import __version__  "
    "# single source of truth; see kinde_sdk/_version.py"
)


_LITERAL_VERSION_LINE = re.compile(
    r'^__version__\s*=\s*["\'][^"\']+["\']\s*$',
    re.MULTILINE,
)


def make_version_dynamic(init_file: Path) -> None:
    """Rewrite the ``__version__`` literal in a generated ``__init__.py``.

    Replaces the OpenAPI-emitted ``__version__ = "X"`` line with
    :data:`DYNAMIC_VERSION_IMPORT` so the sub-package re-exports the
    canonical value from ``kinde_sdk._version`` and can never drift from
    the SDK source of truth.

    Idempotent: a no-op if the file already imports ``__version__`` from
    ``kinde_sdk._version``. Tolerant of missing files and missing
    ``__version__`` lines - logs a warning and returns rather than
    raising, because the calling scripts treat this as a best-effort
    post-generation step.

    Args:
        init_file: Path to the generated sub-package ``__init__.py``.
            Always passed as a :class:`pathlib.Path` (callers convert
            string paths via :func:`pathlib.Path` at the call site).
    """
    if not init_file.exists():
        print(f"⚠️  Cannot rewrite __version__: {init_file} does not exist")
        return

    text = init_file.read_text(encoding="utf-8")

    if "from kinde_sdk._version import __version__" in text:
        print(f"✓ {init_file} already imports __version__ from kinde_sdk._version")
        return

    new_text, n = _LITERAL_VERSION_LINE.subn(
        DYNAMIC_VERSION_IMPORT, text, count=1
    )
    if n == 0:
        print(
            f"⚠️  Could not find a literal __version__ in {init_file} to replace; "
            "is the OpenAPI generator template still emitting one?"
        )
        return

    init_file.write_text(new_text, encoding="utf-8")
    print(f"✓ Rewrote __version__ in {init_file} to import from kinde_sdk._version")


__all__ = [
    "DYNAMIC_VERSION_IMPORT",
    "PACKAGE_VERSION_PLACEHOLDER",
    "SDK_VERSION",
    "make_version_dynamic",
    "read_sdk_version",
]
