#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import pytest
from shapeit.measure import convert, Units


@pytest.mark.parametrize(
    "n,units,to,dimension,n1",
    [
        # linear
        (1, Units.METERS, Units.METERS, 1, 1),
        (1, Units.METERS, Units.KILOMETERS, 1, 0.001),
        (1, Units.KILOMETERS, Units.METERS, 1, 1000),
        (1, Units.KILOMETERS, Units.KILOMETERS, 1, 1),
        (1, Units.METERS, Units.METERS, 2, 1),
        (1, Units.METERS, Units.KILOMETERS, 2, 1e-6),
        (1, Units.KILOMETERS, Units.METERS, 2, 1000000),
        (1, Units.KILOMETERS, Units.KILOMETERS, 2, 1),
        # squares
        (3.14, Units.METERS, Units.METERS, 1, 3.14),
        (3.14, Units.METERS, Units.KILOMETERS, 1, 0.00314),
        (3.14, Units.KILOMETERS, Units.METERS, 1, 3140),
        (3.14, Units.KILOMETERS, Units.KILOMETERS, 1, 3.14),
        (3.14, Units.METERS, Units.METERS, 2, 3.14),
        (3.14, Units.METERS, Units.KILOMETERS, 2, 3.14e-6),
        (3.14, Units.KILOMETERS, Units.METERS, 2, 3140000),
        (3.14, Units.KILOMETERS, Units.KILOMETERS, 2, 3.14)
    ]
)
def test_convert(n, units, to, dimension, n1):
    """
    Arrange/Act: Convert a quantity denominated in one unit to its equivalent
        of another unit.
    Assert: The converted quantity matches the expectation.

    :param n: the original quantity
    :param units: the nominal units
    :param to: the conversion units
    :param dimension: the dimensionality of the original quantity
    :param n1: the expected conversion value
    """
    # Convert to the specified units.
    c = convert(n=n, units=units, to=to, dimension=dimension)
    # Round converted value and the expected value and compare them.
    assert round(c, 8) == round(n1, 8), (
        'The converted value should match the expected value.'
    )