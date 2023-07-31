#!/usr/bin/env python3
"""parameterize a unit test"""
from utils import access_nested_map
from parameterized import parameterized
import unittest


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


if __name__ == "__main__":
    unittest.run()
