#!/usr/bin/env python3
"""parameterize a unit test"""
from utils import access_nested_map
import unittest
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """class to test access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ])
    def test_access_nested_map(self, x, y, expected_result):
        """method that test the access_nested_map"""
        self.assertEqual(access_nested_map(x, y), expected_result)


if __name__ == "__main__":
    unittest.run()
