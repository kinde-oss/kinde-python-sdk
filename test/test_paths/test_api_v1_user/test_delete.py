# # coding: utf-8

# """


#     Generated by: https://openapi-generator.tech
# """

# import unittest
# from unittest.mock import patch

# import urllib3

# import kinde_sdk
# from kinde_sdk.paths.api_v1_user import delete  # noqa: E501
# from kinde_sdk import configuration, schemas, api_client
# from kinde_sdk.test.test_kinde_api_client import TestKindeApiClient

# from .. import ApiTestMixin


# class TestApiV1User(ApiTestMixin, unittest.TestCase):
#     """
#     ApiV1User unit test stubs
#         Delete User  # noqa: E501
#     """
#     _configuration = configuration.Configuration()

#     def setUp(self):
#         kinde_api_client = TestKindeApiClient()
#         kinde_api_client.setUp()
#         # self._configuration.access_token = kinde_api_client.fake_access_token
#         used_api_client = api_client.ApiClient(configuration=self._configuration)
#         self.api = delete.ApiFordelete(api_client=used_api_client)  # noqa: E501

#     def tearDown(self):
#         pass

#     @patch.object(urllib3.PoolManager, 'request')
#     def test_oauth2_v2_user_profile(self, mock_request):
#         mock_request.return_value = self.response(b'')
#         api_response = self.api.delete(skip_deserialization=True)

#         assert isinstance(api_response.response, urllib3.HTTPResponse)
#         assert isinstance(api_response.body, schemas.Unset)
#         assert isinstance(api_response.headers, schemas.Unset)
#         assert api_response.response.status == 200

#     response_status = 200






# if __name__ == '__main__':
#     unittest.main()
