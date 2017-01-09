#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
import sys
import types

def outdated(func):

    #Wraps makes the wrapper function to keep information about the wrapped
    #function.
    @wraps(func)
    def outdated_func(*arguments, **args):
        print(
            "The function \"{0}\" from \"{1}\" has been called but is "
            "outdated.\nNote that it might not function correctly.".format(
                func.__name__,
                sys.modules[func.__module__].__file__))
        return func(*arguments, **args)

    return outdated_func


def accepts(*types):

    def check_accepts(f):

        assert len(types) == f.__code__.co_argcount

        @wraps(f)
        def new_f(*args, **kwds):
            for (a, t) in zip(args, types):
                assert isinstance(a, t), "arg %r does not match %s" % (a, t)

            return f(*args, **kwds)
       #new_f.__name__ = f.__name__
       #new_f.__doc__ = f.__doc__
       #new_f.__module__ = f.__module__
        return new_f
    return check_accepts


def returns(rtype):

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
        # new_f.__name__ = f.__name__
        # new_f.__doc__ = f.__doc__
        # new_f.__module__ = f.__module__
        return new_f
    return check_returns
