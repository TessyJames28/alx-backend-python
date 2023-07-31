#!/usr/bin/env python3
"""test_client module"""
from client import GithubOrgClient
import unittest
from unittest.mock import patch
from parameterized import parameterized


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
