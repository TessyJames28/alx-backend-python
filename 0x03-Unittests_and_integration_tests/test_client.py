#!/usr/bin/env python3
"""
Test case for client.py and fixture.py files
"""
from unittest.mock import patch
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
import unittest
get_json = __import__("utils").get_json


@parameterized.expand([
    ("google"),
    ("abc"),
])

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