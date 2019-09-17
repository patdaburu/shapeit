#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from shapeit.measure import convert, meters, Units


@pytest.mark.parametrize(
    'dimension', [-1, 0, 4]
)
def test_measure_bad_dimension(dimension):
    """
    Arrange/Act: Call the `meters` method with an invalid dimension.
    Assert: The call raises a `ValueError`.

    :param dimension: the dimension
    """
    with pytest.raises(ValueError):
        meters(
            1,
            units=Units.METERS,
            dimension=dimension
        )


@pytest.mark.parametrize(
    'dimension', [-1, 0, 4]
)
def test_convert_bad_dimension(dimension):
    """
    Arrange/Act: Call the `meters` method with an invalid dimension.
    Assert: The call raises a `ValueError`.

    :param dimension: the dimension
    """
    with pytest.raises(ValueError):
        convert(
            1,
            units=Units.METERS,
            to=Units.KILOMETERS,
            dimension=dimension
        )
