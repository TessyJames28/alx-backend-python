#!/usr/bin/env python3
"""test_client module"""
from client import GithubOrgClient
import unittest
from unittest.mock import patch
from parameterized import parameterized
from utils import get_json


class TestGithubOrgClient(unittest.TestCase):
    """class to test GithubOrgClient class"""

    @parameterized.expand([
        ("google"),
        ("abc"),
        ])
    def test_org(self, x):
        """test that GithubOrgClient.org returns the correct value"""

        with patch("client.GithubOrgClient.org") as mock_response:
            GithubOrgClient.ORG_URL = x
            GithubOrgClient.org()
            mock_response.assert_called_once()

    def test_public_repos_url(self):
        """test public_repo_url"""

        with patch("client.GithubOrgClient._public_repos_url") as mock_respons:
            mock_respons.return_value = "abc.com"
            self.assertEquals(GithubOrgClient._public_repos_url(), "abc.com")

    def test_public_repos(self):
        """test public_repos"""
        with patch('client.GithubOrgClient.public_repos') as mock_response:
            mock_response.return_value = 'github.com'
            result = GithubOrgClient.public_repos()
            self.assertEqual(result, 'github.com')
            mock_response.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ])
    def test_has_license(self, x, y, expected_result):
        """test and parameterize has_license"""
        self.assertEquals(GithubOrgClient.has_license(x, y), expected_result)
