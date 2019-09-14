#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import pytest
from shapeit import SrGeometry, SrPoint, WGS_84


@pytest.fixture(scope='module', name='wgs84_point')
def wgs84_point_fix() -> SrPoint:
    """
    Get a WGS-84 `SrPoint`.

    :return: the point
    """
    return SrPoint.from_lat_lon(lat=45.553670, lon=-94.142430)


@pytest.mark.parametrize(
    'sr_point',
    [
        SrPoint.from_lat_lon(lat=45.553670, lon=-94.142430),
    ]
)
def test_export_load(sr_point):
    """
    Arrange: Export an `SrPoint` to JSON.
    Act: Load the export data to create a new `SrPoint`.
    Assert: The loaded `SrPoint` is equivalent to the original.

    :param sr_point: an `SrPoint`
    :return:
    """
    exported = sr_point.export()
    exported_json = json.dumps(exported)
    loaded = SrGeometry.load(json.loads(exported_json))
    assert loaded == sr_point
    assert hash(loaded) == hash(sr_point)


def test_properties_wgs84(wgs84_point):
    """
    Arrange/Act: Retrieve the WGS-84 figure point.
    Assert: Properties and zero-argument methods return expected values.

    :param wgs84_point: the WGS-84 fixture point
    """
    assert wgs84_point.sr == WGS_84
    assert wgs84_point.srid == 4326
    assert wgs84_point.x == wgs84_point.point.x
    assert wgs84_point.y == wgs84_point.point.y
    assert wgs84_point.location() == wgs84_point
    assert wgs84_point.as_wgs84() == wgs84_point


@pytest.mark.parametrize(
    'point,utm_zone',
    [
        (SrPoint.from_lat_lon(lat=45.553670, lon=-94.142430), 32615),
        (SrPoint.from_coords(x=410830.54, y=5045093.81, sr=32615), 32615)
    ]
)
def test_as_utm(point, utm_zone):
    """
    Arrange: Start with a point.
    Act: Call the `as_utm` method to get the point transformed in the
        appropriate UTM coordinate reference system.
    Assert: The coordinate system ID (SRID) of the transformed coordinate
        matches the expectation.

    :param point: the point
    :param utm_zone: the expected UTM zone SRID
    """
    utm_point = point.as_utm()
    assert utm_point.srid == utm_zone
