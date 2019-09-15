#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 5/8/19 by Pat Daburu
"""
.. currentmodule:: shapeit.distance
.. moduleauthor:: Pat Daburu <pat@daburu.net>

This module deals with linear distance measurements.
"""
from enum import Enum
import math
from typing import Dict


class Units(Enum):
    """
    These are common distance units.
    """
    METERS = 'meters'  #: meters
    KILOMETERS = 'kilometers'  #: kilometers


_meter_conversions: Dict[Units, float] = {
    Units.METERS: 1.0,  # 1 meter = 1 meter
    Units.KILOMETERS: 1000.0  # 1 kilometer = 1000 meters
}  #: conversion factors from meters to other linear distance units


def meters(n: float, units: Units, dimension: int = 1) -> float:
    """
    Convert a linear distance to its equivalent in meters.

    :param n: the quantity
    :param units: the units in which the distance is expressed
    :param dimension: the dimensions of the measurement
    :return: the equivalent quantity in meters

    .. seealso::

        :py:class:`Units`
    """
    if dimension < 1 or dimension > 3:
        raise ValueError("'dimension' must be between 1 and 3.")
    return n * (math.pow(_meter_conversions[units], dimension))


def convert(
        n: float,
        units: Units,
        to: Units,
        dimension: int = 1
) -> float:
    """
    Convert a quantity defined in one unit to its equivalent quantity in another
    unit.

    :param n: the quantity
    :param units: the units
    :param to: the conversion units
    :param dimension: the dimensionality of `n`
    :return: the equivalent units
    :raises ValueError: if the ``dimension`` parameter is not ``1``, ``2``, or
        ``3``

    .. note::

        If the units represent a square (*e.g.* "square meters"), the
        ``dimension`` parameter should be ``2``.  If it's cubic
        (*e.g.* "cubic meters"), ``dimension`` should be ``3``.  For linear
        distances, use the default (``1``).
    """
    # Sanity Check:  If the original units and the target units are the same...
    if units == to:
        # ...just return the original quantity.
        return n
    if dimension < 1 or dimension > 3:
        raise ValueError("'dimension' must be between 1 and 3.")
    # Get the quantity in meters.  Notice that if we're working with 2
    # dimensions (squares) or 3 dimensions (cubes) we only want the length
    # of one "side".
    m1d = meters(
        n=(
            n if dimension == 1
            else math.pow(n, (1.0/float(dimension)))  # nth root
        ),
        units=units,
        dimension=1  # We've already reduced `n` to one dimension.
    )
    # Convert the 1-dimensional length in meters to its equivalent in the
    # target units.
    to1d = m1d/_meter_conversions[to]
    # Now restore the original dimensionality and return the value.
    return (
        to1d if dimension == 1
        else math.pow(to1d, dimension)
    )
