#!/usr/bin/env python3
"""parameterize a unit test"""
from utils import access_nested_map, get_json
from parameterized import parameterized
import unittest
from unittest import mock


class TestAccessNestedMap(unittest.TestCase):
    """class to test access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ])
    def test_access_nested_map(self, x, y, expected_result):
        """method that test the access_nested_map"""
        self.assertEquals(access_nested_map(x, y), expected_result)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
        ])
    def test_access_nested_map_exception(self, x, y, expected_result):
        """assert that the function raises error"""
        with self.assertRaises(expected_result):
            access_nested_map(x, y)


class TestGetJson(unittest.TestCase):
    """class to test get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
        ])
    def test_get_json(self, x, expected_result):
        """return a Mock object with a json method that returns test_payload"""
        with mock.patch("requests.get") as mock_response:
            result = get_json(x)
            mock_response.json.return_value = expected_result
            mock_response.assert_called_once_with(x)


if __name__ == "__main__":
    unittest.run()
