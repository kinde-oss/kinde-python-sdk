# coding: utf-8

"""
    Kinde Management API

    Provides endpoints to manage your Kinde Businesses  # noqa: E501

    The version of the OpenAPI document: 1
    Contact: support@kinde.com
    Generated by: https://openapi-generator.tech
"""

import unittest

import kinde_sdk
from kinde_sdk.model.connected_apps_auth_url import ConnectedAppsAuthUrl
from kinde_sdk.management import schemas


class TestConnectedAppsAuthUrl(unittest.TestCase):
    """ConnectedAppsAuthUrl unit test stubs"""

    def test_connected_apps_auth_url(self):
        inst = ConnectedAppsAuthUrl({})
        with self.assertRaises(KeyError):
            inst["url"]
        assert inst.get_item_oapg("url") is schemas.unset
        with self.assertRaises(AttributeError):
            inst.url

        inst = ConnectedAppsAuthUrl(url="")
        url = inst["url"]
        assert url == ""


if __name__ == "__main__":
    unittest.main()
