# coding: utf-8

"""


    Generated by: https://openapi-generator.tech
"""

import unittest
from unittest.mock import patch

import urllib3

import kinde_sdk
from kinde_sdk.paths.oauth2_v2_user_profile import get  # noqa: E501
from kinde_sdk import configuration, schemas, api_client

from .. import ApiTestMixin


class TestOauth2V2UserProfile(ApiTestMixin, unittest.TestCase):
    """
    Oauth2V2UserProfile unit test stubs
        Returns the details of the currently logged in user  # noqa: E501
    """

    _configuration = configuration.Configuration()

    def setUp(self):
        used_api_client = api_client.ApiClient(configuration=self._configuration)
        self.api = get.ApiForget(api_client=used_api_client)  # noqa: E501

    def tearDown(self):
        pass

    response_status = 200


if __name__ == "__main__":
    unittest.main()