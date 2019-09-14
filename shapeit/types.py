#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 7/7/19
"""
.. currentmodule:: shapeit.types
.. moduleauthor:: Pat Daburu <pat@daburu.net>


If you're dealing with Python types, deal here.
"""
import importlib
import sys
from typing import TypeVar
from .errors import ShapeitException


class InvalidTypeException(ShapeitException):
    """
    Raised when an attempt is made to retrieve an non-existent type from a
    fully-qualified name.

    .. seealso::

        :py:func:`pycls <pycls>`
    """


def pyfqn(obj) -> str:
    """
    Get the fully-qualified name (FQN) of an object's type.

    :param obj: the object
    :return: the fully-qualified type name
    """
    return f"{obj.__class__.__module__}.{obj.__class__.__name__}"


def pycls(fqn_: str) -> TypeVar:
    """
    Get the class to which a fully-qualified name (FQN) refers.

    :param fqn_: the fully-qualified name of the class
    :return: the class described by the fully-qualified name (FQN)
    """
    # Split up the fqn (fully-qualified name) at the dots.
    tokens = fqn_.split('.')
    # Put the module name back together.
    modname = '.'.join(tokens[:-1])
    # Let's get the module in which
    try:
        mod = sys.modules[modname]
    except KeyError:
        mod = importlib.import_module(modname)
    # The name of the class is the last token.  Retrieve it from the module.
    _cls = getattr(mod, tokens[-1])
    # That's our answer.
    return _cls
