#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from shapely.geometry import (
    Point,
    LineString,
    Polygon,
    MultiPoint,
    MultiLineString,
    MultiPolygon
)
from shapeit import (
    sr_shape,
    SrPoint,
    SrPolyline,
    SrPolygon,
    SrMultiPoint,
    SrMultiPolyline,
    SrMultiPolygon
)
from shapeit.srs import Sr


@pytest.mark.parametrize(
    'base_geometry,sr,sr_geom_type',
    [
        (Point(0.0, 0.0), 4326, SrPoint),
        (Point(0.0, 0.0), 3857, SrPoint),
        (LineString([(0, 0), (1, 1)]), 3857, SrPolyline),
        (Polygon([(0, 0), (1, 1), (1, 0)]), 32619, SrPolygon),
        (
            MultiPoint([(0, 0), (1, 1), (0, 2), (2, 2), (3, 1), (1, 0)]),
            3857,
            SrMultiPoint
        ),
        (
            MultiLineString([((0, 0), (1, 1)), ((-1, 0), (1, 0))]),
            3857,
            SrMultiPolyline
        ),
        (
            MultiPolygon([Point(i, 0).buffer(0.7) for i in range(5)]),
            3857,
            SrMultiPolygon
        )
    ]
)
def test_sr_shape(base_geometry, sr, sr_geom_type):
    """
    Arrange/Act: Create an `SrGeometry` from a base geometry and spatial
        reference using the `sr_shape` function.
    Assert: The `SrGeometry` instance type and SRID match the expectations.

    :param base_geometry: the base geometry (or mapping)
    :param sr: the spatial reference
    :param sr_geom_type: the expected `SrGeometry` type
    """
    sr_geom = sr_shape(
        base_geometry=base_geometry,
        sr=sr
    )
    assert type(sr_geom) == sr_geom_type
    srid = sr.srid if isinstance(sr, Sr) else sr
    assert srid == sr_geom.srid
