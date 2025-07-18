# coding: utf-8

"""
    Kinde Management API

     Provides endpoints to manage your Kinde Businesses.  ## Intro  ## How to use  1. [Set up and authorize a machine-to-machine (M2M) application](https://docs.kinde.com/developer-tools/kinde-api/connect-to-kinde-api/).  2. [Generate a test access token](https://docs.kinde.com/developer-tools/kinde-api/access-token-for-api/)  3. Test request any endpoint using the test token 

    The version of the OpenAPI document: 1
    Contact: support@kinde.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from kinde_sdk.management.models.event_type import EventType
from typing import Optional, Set
from typing_extensions import Self

class GetEventTypesResponse(BaseModel):
    """
    GetEventTypesResponse
    """ # noqa: E501
    code: Optional[StrictStr] = Field(default=None, description="Response code.")
    message: Optional[StrictStr] = Field(default=None, description="Response message.")
    event_types: Optional[List[EventType]] = None
    __properties: ClassVar[List[str]] = ["code", "message", "event_types"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of GetEventTypesResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in event_types (list)
        _items = []
        if self.event_types:
            for _item_event_types in self.event_types:
                if _item_event_types:
                    _items.append(_item_event_types.to_dict())
            _dict['event_types'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GetEventTypesResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "code": obj.get("code"),
            "message": obj.get("message"),
            "event_types": [EventType.from_dict(_item) for _item in obj["event_types"]] if obj.get("event_types") is not None else None
        })
        return _obj


