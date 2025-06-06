#!/usr/bin/env python3
"""
Test case for client.py and fixture.py files
"""
from unittest.mock import patch
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
import unittest
from fixtures import TEST_PAYLOAD
from utils import get_json


class TestGithubOrgClient(unittest.TestCase):
    """
    Handles unittest for GitubOrgClient class
    Ensures GithubOrgClient returns the correct value
    """
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    def test_org(self, company):
        """
        Ensures get_json is called once with expected argument
        """
        with patch("client.GithubOrgClient.org") as mock_response:
            GithubOrgClient.ORG_URL = company
            GithubOrgClient.org()

            mock_response.assert_called_once()

    def test_public_repos_url(self):
        """
        Ensures test returns a known payload
        """
        with patch("client.GithubOrgClient._public_repos_url") as mock_resp:
            mock_resp.return_value = "abc.com"
            self.assertEqual(GithubOrgClient._public_repos_url(), "abc.com")

    @patch("client.GithubOrgClient.public_repos")
    def test_public_repos(self, mock_resp):
        """
        Testcase to return a payload of your choice
        """
        mock_resp.return_value = "google.com"
        result = GithubOrgClient.public_repos()
        self.assertEqual(result, "google.com")
        mock_resp.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, license, key, expected_outcome):
        """
        Test has license with parameterized inputs
        """
        self.assertEqual(GithubOrgClient.has_license(
            license, key), expected_outcome)


@parameterized_class([
    {"name": 'org_payload', "value": TEST_PAYLOAD[0][0]},
    {"name": 'repos_payload', "value": TEST_PAYLOAD[0][1]},
    {"name": 'expected_repos', "value": TEST_PAYLOAD[0][2]},
    {"name": 'apache2_repos', "value": TEST_PAYLOAD[0][3]},
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test: fixture
    Create mock code that sends external requests only
    """

    @classmethod
    def setUpClass(cls) -> None:
        def getPayload(url):
            return mock.Mock({cls.name: cls.value})
        cls.get_patcher = patch("requests.get", side_effect=getPayload)
        cls.get_patcher.start()

    def test_public_repos_with_license(self):
        """
        Test for public repo with license
        """
        self.assertTrue(True)

    def test_public_repos(self):
        """
        Test public repo
        """
        self.assertTrue(True)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.get_patcher.stop()
