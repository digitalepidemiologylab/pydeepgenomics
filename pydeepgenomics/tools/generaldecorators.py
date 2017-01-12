#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contains decorators used in some of the packages of this
project and for development.

The decorators designed in this modules are not specific to the project and
can be used elsewhere. They offer some features to make the code look cleaner
(*e.g.* control the types of the arguments given to a function) or to help
development (*e.g.* label outdated functions still present in the code and
some other tools coming in future versions)
"""
import doctest
from functools import wraps


def outdated(func):
    """Mark a function as outdated and signals it to the user if the function
    is called.

    Args:
        func (:obj:`function`): function to be wrapped in this decorator

    Returns:
        outdated_func (:obj:`function`): wrapped function

    Examples:
            >>> @outdated
            ... def func():
            ...     pass
            >>> func()
            The function "func" has been called but is outdated.
            Note that it might not function correctly.
    """
    # Wraps makes the wrapper function to keep information about the wrapped
    # function.
    @wraps(func)
    def outdated_func(*arguments, **args):
        print(
            "The function \"{0}\" has been called but is "
            "outdated.\nNote that it might not function correctly.".format(
                func.__name__))
        return func(*arguments, **args)

    return outdated_func


def accepts(*types):
    """Compare the type of the arguments given to the function with some
    "reference" types specified to the decorator.

    Args:
        *types (:obj:`type`): "Reference" types which will be compared to the\
         ones given to the wrapped function.

    Returns:
        check_accepts (:obj:`function`): wrapped function

    Raises:
        AssertionError: When the arguments given to the wrapped function are
         not of the types given to the wrapper or when too many arguments are
         given to the wrapped function.

    Examples:
        Function which accepts only one argument of one specific type:
            >>> @accepts(int)
            ... def func(x):
            ...     pass
            >>> func(1)
            >>> try:
            ...     func("a")
            ... except AssertionError:
            ...     print("Incorrect type !")
            Incorrect type !

        Function which accepts multiple :
            >>> @accepts(str, (list, tuple))
            ... def func(x, y):
            ...     pass
            >>> func("foo", (1, 2, 3))
            >>> func("bar", [1, 2, 3])
            >>> try:
            ...     func("foo", {"a": 1, "b": 2, "c": 3})
            ... except AssertionError:
            ...     print("Incorrect type !")
            Incorrect type !
            >>> try:
            ...     func((1, 2, 3), "foo")
            ... except AssertionError:
            ...     print("The order of the  parameters matters!")
            The order of the  parameters matters!
    """
    def check_accepts(f):

        assert len(types) == f.__code__.co_argcount

        @wraps(f)
        def new_f(*args, **kwds):
            for (a, t) in zip(args, types):
                assert isinstance(a, t), "arg %r does not match %s" % (a, t)

            return f(*args, **kwds)

        return new_f
    return check_accepts


def returns(rtype):
    """Compare the type of the object returned by the wrapped function with
    a "reference" type specified to the decorator.

    Args:
        rtype (:obj:`type`): "Reference" types which will be compared to the\
         ones given to the wrapped function.

    Returns:
        check_returns (:obj:`function`): wrapped function

    Raises:
        AssertionError: When the arguments given to the wrapped function are
         not of the types given to the wrapper.

    Examples:
        Function which accepts only one argument of one specific type:
            >>> @returns(int)
            ... def func():
            ...     return 1
            >>> func()
            1
            >>> @returns(int)
            ... def func():
            ...     return "a"
            >>> try:
            ...     func()
            ... except AssertionError:
            ...     print("Incorrect return type !")
            Incorrect return type !

    """
    def check_returns(f):
        @wraps(f)
        def new_f(*args, **kwds):
            result = f(*args, **kwds)
            if rtype is not None:
                assert isinstance(result, rtype), \
                    "return value %r does not match %s" % (result, rtype)
                return result
            else:
                assert result is None
                return result

        return new_f
    return check_returns

if __name__ == "__main__":
    doctest.testmod()
    print(__doc__)