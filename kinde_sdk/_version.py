"""Single source of truth for the Kinde Python SDK version.

This module is intentionally minimal: it must not import anything else,
so it can be safely imported from any sub-package's ``__init__`` without
risking a circular import with ``kinde_sdk/__init__.py``.

Derived surfaces (all kept in sync from this string):

* ``kinde_sdk.__version__`` re-exports it directly.
* The generated ``kinde_sdk/management/__init__.py`` and
  ``kinde_sdk/frontend/__init__.py`` re-export it via a post-generation
  rewrite, so all three namespaces report the same version.
* ``pyproject.toml`` resolves its dynamic version from this attribute,
  so distribution metadata (and the ``SDKTracker`` User-Agent) matches.
* Both OpenAPI generator configs - ``openapitools.json`` (management,
  tracked in git) and ``generator/frontend_config.yaml`` (frontend,
  transient and rewritten on each generator run) - intentionally store
  the literal placeholder ``"SDK_VERSION"`` in their ``packageVersion``
  field rather than a version literal, so neither file can be mistaken
  for a second source of truth. The resolved value is injected at
  runtime by the respective wrapper script via
  ``--additional-properties=packageVersion=<SDK_VERSION>`` on the
  ``openapi-generator-cli`` command line, and the post-generation
  ``make_version_dynamic`` rewrite imports ``__version__`` from this
  module so the placeholder never reaches a wrapper-generated artifact.
  ``testv2/testv2_core/test_version_sync.py`` enforces both placeholder
  invariants in CI.

Bump this string on every release; nothing else needs touching by hand.
After bumping, run both generator scripts (or rely on a release pipeline
that does) so any regenerated sub-package files are committed alongside.
The generator-config files themselves are unaffected by the bump - they
permanently hold the ``"SDK_VERSION"`` placeholder.
"""

__version__ = "2.3.1"
