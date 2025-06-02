#!/usr/bin/env python3
"""Test case for utils.py file
unittest for access_nested_map
"""
access_nested_map = __import__("utils").access_nested_map
from parameterized import parameterized, parameterized_class
import unittest


class TestAccessNestedMap(unittest.TestCase):
    """
    Unittest for access nested map
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])

    
    def test_access_nested_map(self, nested_map, path, result):
        """test cases for access nested map method
        """
        self.assertEqual(access_nested_map(nested_map, path), result)


if __name__ == '__main__':
    unittest.main()
