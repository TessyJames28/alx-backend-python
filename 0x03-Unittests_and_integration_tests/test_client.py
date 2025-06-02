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