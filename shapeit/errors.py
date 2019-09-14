#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 6/29/19
"""
.. currentmodule:: shapeit.errors
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Sometimes things go wrong.
"""


class ShapeitException(Exception):
    """
    This is the base exception for other exceptions defined in this library.
    """
    def __init__(self, message: str, inner: Exception = None):
        """

        :param message: the exception message
        :param inner: the exception that caused this exception
        """
        super().__init__(message)
        self._message = message
        self._inner = inner

    @property
    def message(self) -> str:
        """
        Get the exception message.
        """
        return self._message

    @property
    def inner(self) -> Exception or None:
        """
        Get the exception that caused this exception.
        """
        return self._inner
