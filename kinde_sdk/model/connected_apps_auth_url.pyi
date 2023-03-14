# coding: utf-8

"""
    Kinde Management API

    Provides endpoints to manage your Kinde Businesses  # noqa: E501

    The version of the OpenAPI document: 1
    Contact: support@kinde.com
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from kinde_sdk import schemas  # noqa: F401

class ConnectedAppsAuthUrl(schemas.DictSchema):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    class MetaOapg:
        class properties:
            url = schemas.StrSchema
            session_id = schemas.StrSchema
            __annotations__ = {
                "url": url,
                "session_id": session_id,
            }
    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["url"]
    ) -> MetaOapg.properties.url: ...
    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["session_id"]
    ) -> MetaOapg.properties.session_id: ...
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    def __getitem__(
        self,
        name: typing.Union[
            typing_extensions.Literal[
                "url",
                "session_id",
            ],
            str,
        ],
    ):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["url"]
    ) -> typing.Union[MetaOapg.properties.url, schemas.Unset]: ...
    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["session_id"]
    ) -> typing.Union[MetaOapg.properties.session_id, schemas.Unset]: ...
    @typing.overload
    def get_item_oapg(
        self, name: str
    ) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    def get_item_oapg(
        self,
        name: typing.Union[
            typing_extensions.Literal[
                "url",
                "session_id",
            ],
            str,
        ],
    ):
        return super().get_item_oapg(name)
    def __new__(
        cls,
        *_args: typing.Union[
            dict,
            frozendict.frozendict,
        ],
        url: typing.Union[MetaOapg.properties.url, str, schemas.Unset] = schemas.unset,
        session_id: typing.Union[
            MetaOapg.properties.session_id, str, schemas.Unset
        ] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[
            schemas.AnyTypeSchema,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            None,
            list,
            tuple,
            bytes,
        ],
    ) -> "ConnectedAppsAuthUrl":
        return super().__new__(
            cls,
            *_args,
            url=url,
            session_id=session_id,
            _configuration=_configuration,
            **kwargs,
        )