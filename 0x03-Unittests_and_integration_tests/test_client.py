#!/usr/bin/env python3
"""
Test case for client.py and fixture.py files
"""
from unittest.mock import patch
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
import unittest
get_json = __import__("utils").get_json


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
