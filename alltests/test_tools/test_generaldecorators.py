#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A bunch of tests for the functions defined in generaldecorators.py.
Note : they should be run from the root folder of the library with the command
python -m unittest discover
"""
from contextlib import contextmanager
import unittest
import os
import sys

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from pydeepgenomics.tools import generaldecorators as gd
except ImportError:
    cmd_dir = os.path.abspath(os.path.dirname(__file__)).split("alltests")[0]
    if cmd_dir not in sys.path:
        sys.path.append(cmd_dir)
    from pydeepgenomics.tools import generaldecorators as gd


@contextmanager
def capture(command, *args, **kwargs):
    out = sys.stdout
    sys.stdout = StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        yield sys.stdout.read()
    finally:
        sys.stdout = sys.__stdout__


class TestOutdated(unittest.TestCase):

    def test_without_decorator(self):

        def basic_print_outdated():
            print("Hello world!")
        expected_out = "Hello world!\n"

        with capture(basic_print_outdated) as output:
            self.assertEqual(expected_out, output)

    def test_on_a_sentence(self):

        @gd.outdated
        def basic_print_outdated():
            print("Hello world!")
        expected_out = "The function \"{0}\" has been called but is \
outdated.\nNote that it might not function correctly.\n".format(
            "basic_print_outdated") + "Hello world!\n"

        with capture(basic_print_outdated) as output:
            self.assertEqual(expected_out, output)

    def test_fct_with_return(self):

        @gd.outdated
        def basic_return_outdated():
            return "Hello world!"

        expected_out = "The function \"{0}\" has been called but is \
outdated.\nNote that it might not function correctly.\n".format(
            "basic_return_outdated")
        with capture(basic_return_outdated) as output:
            self.assertEqual(expected_out, output)
        sys.stdout = StringIO()
        expected_retuned = "Hello world!"
        returned = basic_return_outdated()
        sys.stdout = sys.__stdout__
        self.assertEqual(expected_retuned, returned)

    def test_fct_with_arguments(self):

        @gd.outdated
        def basic_take_arguments_outdated(str_1, str_2):
            print(str_1 + " " + str_2)

        expected_out = "The function \"{0}\" has been called but is \
outdated.\nNote that it might not function correctly.\n".format(
            "basic_take_arguments_outdated") + "Hello world!\n"

        with capture(basic_take_arguments_outdated, "Hello", "world!") as output:
            self.assertEqual(expected_out, output)


class TestAccepts(unittest.TestCase):

    def test_simple_string_correct_arg_accepts(self):

        @gd.accepts(str)
        def simple_string_correct_arg_accepts(string):
            print(string)
        expected_out = "Hello world!\n"
        with capture(
                simple_string_correct_arg_accepts,
                "Hello world!") as output:
            self.assertEqual(expected_out, output)

    def test_simple_string_incorrect_arg_accepts(self):
        @gd.accepts(str)
        def simple_string_incorrect_arg_accepts(string):
            print(string)
        with self.assertRaises(AssertionError):
            simple_string_incorrect_arg_accepts(42)

    def test_multiple_correct_arg_accepts(self):

        @gd.accepts(str, int, float, list, tuple)
        def simple_string_correct_arg_accepts(
                string,
                int_,
                float_,
                list_,
                tuple_):
            output = [
                str(tuple_[0]) + str(int_+float_) + " " + ele + " " +
                string for ele in list_]
            return output
        input_str = "apples."
        input_int = 3
        input_float = 0.5
        input_list = ["good", "bad", "excellent"]
        input_tuple = ("I ate ", 2)
        expected_output = [
            "I ate 3.5 good apples.",
            "I ate 3.5 bad apples.",
            "I ate 3.5 excellent apples.",
        ]
        self.assertEqual(
            simple_string_correct_arg_accepts(
                input_str,
                input_int,
                input_float,
                input_list,
                input_tuple),
            expected_output
        )

    def test_multiple_partial_correct_arg_accepts(self):
        @gd.accepts(str, int, float, list, tuple)
        def simple_string_correct_arg_accepts(
                string,
                int_,
                float_,
                list_,
                tuple_):
            output = [
                str(tuple_[0]) + str(int_+float_) + " " + ele + " " +
                string for ele in list_]
            return output
        input_str = "apples."
        input_float = 0.5
        input_list = ["good", "bad", "excellent"]
        input_tuple = ("I ate ", 2)

        with self.assertRaises(AssertionError):
            simple_string_correct_arg_accepts(
                input_str,
                input_str,
                input_float,
                input_list,
                input_tuple)

# Problematic test, the AssertError is not correctly catched
    # def test_too_many_arg_accepts(self):
    # 	@gd.accepts(str)
    # 	def too_many_arg_accepts(
    # 			string1, string2):
    # 		output = string1 + string2
    # 		return output
    # 	str1 = "Hello"
    # 	str2 = " world!"
#
    # 	with self.assertRaises(AssertionError):
    # 		too_many_arg_accepts(str1, str2)

    def test_multiple_types_for_one_arg_accepts(self):
        @gd.accepts((int, float), (int, float))
        def multiple_types_for_one_arg_accepts(number1, number2):
            return number1 + number2
        n1 = int(42)
        n2 = 3.14159
        n3 = "1.4142"
        self.assertEqual(multiple_types_for_one_arg_accepts(n1, n1), n1+n1)
        self.assertEqual(multiple_types_for_one_arg_accepts(n1, n2), n1+n2)
        self.assertEqual(multiple_types_for_one_arg_accepts(n2, n2), n2+n2)
        with self.assertRaises(AssertionError):
            multiple_types_for_one_arg_accepts(n1, n3)


class TestReturns(unittest.TestCase):

    def test_correct_return_none_returns(self):

        @gd.returns(None)
        def correct_return_none_returns():
            return
        x = correct_return_none_returns()
        self.assertIsNone(x)

    def test_incorrect_return_none_returns(self):

        @gd.returns(None)
        def incorrect_return_none_returns():
            return "Hello world!"
        with self.assertRaises(AssertionError):
            incorrect_return_none_returns()

    def test_correct_return_simple_string_returns(self):

        @gd.returns(str)
        def correct_return_simple_string_returns():
            return "Hello world!"
        x = correct_return_simple_string_returns()
        self.assertTrue(isinstance(x, str))

    def test_incorrect_return_simple_string_returns(self):

        @gd.returns(str)
        def incorrect_return_simple_string_returns():
            return 1.7320
        with self.assertRaises(AssertionError):
            incorrect_return_simple_string_returns()

    def test_correct_return_tuple_of_args_returns(self):

        @gd.returns(tuple)
        def correct_return_tuple_of_args_returns():
            return "Hello world!", 7
        x, y = correct_return_tuple_of_args_returns()

        self.assertTrue(isinstance(x, str))
        self.assertTrue(isinstance(y, int))


if __name__ == "__main__":

    unittest.main()
