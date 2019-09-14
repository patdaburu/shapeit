#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 5/12/19 by Pat Blair
"""
.. currentmodule:: shapeit.xchg
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Document exchange... data exchange... it all starts here!
"""
from abc import ABC, abstractmethod
from typing import Any, Mapping


class Exportable(ABC):
    """
    Objects that can be exported as and loaded from simple data types
    should extend `Exportable` to make their intentions clear and their
    methods consistent.
    """
    @abstractmethod
    def export(self) -> Mapping[str, Any]:
        """
        Export the instance as a mapping of simple types.

        :return: the mapping
        """

    @classmethod
    @abstractmethod
    def load(cls, data: Mapping[str, Any]) -> Any:
        """
        Create an instance from a mapping.

        :param data: the data
        :return: the instance
        """
