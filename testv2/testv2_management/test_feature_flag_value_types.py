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

    generator.apply_spec_errata({"output_dir": str(tmp_path)})
    patched = target.read_text()
    assert "Optional[Union[StrictBool, StrictInt, StrictStr]]" in patched
    assert "StrictBool, StrictInt, StrictStr, field_validator" in patched

    generator.apply_spec_errata({"output_dir": str(tmp_path)})
    assert target.read_text() == patched
