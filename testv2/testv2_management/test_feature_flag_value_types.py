"""Feature flag values come back typed (bool, int or str), not always as strings."""
import pytest

from kinde_sdk.management.models.get_environment_feature_flags_response import GetEnvironmentFeatureFlagsResponse
from kinde_sdk.management.models.get_organization_feature_flags_response import GetOrganizationFeatureFlagsResponse


API_RESPONSE = {
    "code": "OK",
    "message": "Success",
    "feature_flags": {
        "dark_mode": {"type": "bool", "value": True},
        "social_media": {"type": "bool", "value": False},
        "max_projects": {"type": "int", "value": 5},
        "theme": {"type": "str", "value": "dark"},
    },
}


@pytest.mark.parametrize("model", [GetEnvironmentFeatureFlagsResponse, GetOrganizationFeatureFlagsResponse])
def test_typed_flag_values_parse(model):
    flags = model.from_dict(API_RESPONSE).feature_flags
    assert flags["dark_mode"].value is True
    assert flags["social_media"].value is False
    assert flags["max_projects"].value == 5
    assert flags["theme"].value == "dark"
    assert model.from_dict(API_RESPONSE).to_dict() == API_RESPONSE


def test_generator_erratum_patches_generated_model(tmp_path):
    import generate_management_sdk as generator

    target = tmp_path / "models" / "get_organization_feature_flags_response_feature_flags_value.py"
    target.parent.mkdir()
    generated = (
        "from pydantic import BaseModel, ConfigDict, StrictStr, field_validator\n"
        "from typing import Any, ClassVar, Dict, List, Optional\n"
        "class M(BaseModel):\n"
        "    value: Optional[StrictStr] = None\n"
    )
    target.write_text(generated)

    assert generator.apply_spec_errata({"output_dir": str(tmp_path)})
    patched = target.read_text()
    assert "Optional[Union[StrictBool, StrictInt, StrictStr]]" in patched
    assert "StrictBool, StrictInt, StrictStr, field_validator" in patched
    assert "from typing import Any, ClassVar, Dict, List, Optional, Union\n" in patched

    assert generator.apply_spec_errata({"output_dir": str(tmp_path)})
    assert target.read_text() == patched


@pytest.mark.parametrize("generated", [
    None,  # the model file is missing
    "from pydantic import BaseModel\nclass M(BaseModel):\n    value: Optional[StrictStr] = Field(default=None)\n",
])
def test_generator_fails_when_erratum_cannot_be_applied(tmp_path, generated):
    import generate_management_sdk as generator

    if generated is not None:
        target = tmp_path / "models" / "get_organization_feature_flags_response_feature_flags_value.py"
        target.parent.mkdir()
        target.write_text(generated)

    assert generator.apply_spec_errata({"output_dir": str(tmp_path)}) is False


def test_generation_fails_when_erratum_cannot_be_applied(monkeypatch):
    import generate_management_sdk as generator

    monkeypatch.setattr(generator, "generate_sdk", lambda config: True)
    monkeypatch.setattr(generator, "fix_imports", lambda config: None)
    monkeypatch.setattr(generator, "make_version_dynamic", lambda path: None)
    monkeypatch.setattr(generator, "add_custom_imports", lambda config: None)
    monkeypatch.setattr(generator, "apply_spec_errata", lambda config: False)
    later_steps = []
    monkeypatch.setattr(generator, "validate_generation", lambda config: later_steps.append("validate") or True)
    monkeypatch.setattr(generator, "run_tests", lambda config: later_steps.append("tests") or True)
    monkeypatch.setattr(generator, "show_diff", lambda config: later_steps.append("diff"))

    assert generator.generate_single_sdk(skip_tests=False, no_diff=False) is False
    assert later_steps == []
