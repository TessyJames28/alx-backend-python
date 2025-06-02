#!/usr/bin/env python3
"""Test case for utils.py file
unittest for access_nested_map
"""
access_nested_map = __import__("utils").access_nested_map
utils = __import__("utils")
get_json = __import__("utils").get_json
memoize = __import__("utils").memoize
import unittest.mock
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


    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])

    def test_access_nested_map_exception(self, nested_map, path, expected_exception):
        """
        Tests that the proper exception is raised
        Raises KeyError exception
        """
        with self.assertRaises(expected_exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Handles http call mockup test
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])

    @unittest.mock.patch("utils.requests.get")
    def test_get_json(self, url, test_payload, mock_get):
        """
        Test the return payload with a mockup test
        """
        mock_get.return_value.json.return_value = test_payload

        result = get_json(url)

        self.assertEqual(result,test_payload)

        mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """
    Test cases for the memoize function
    Parameterized and patched
    """
    def test_memoize(self):
        """
        Test for memoize function
        """

        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
        
        my_class = TestClass()

        with unittest.mock.patch.object(my_class, 'a_method') as mock_test:
            my_class.a_property()
            my_class.a_property()
            mock_test.assert_called_once()
        

if __name__ == '__main__':
    unittest.main()
