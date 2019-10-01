#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from shapeit import SrPoint, MetricProjections


@pytest.mark.parametrize(
    'geometry,radius,resolution,metric_projection,area_m',
    [
        (
            SrPoint.from_lat_lon(lat=45.553670, lon=-94.142430),
            5,
            1000,
            MetricProjections.WEB_MERCATOR,
            78.5397
        ),
        (
            SrPoint.from_lat_lon(lat=45.553670, lon=-94.142430),
            5,
            1000,
            MetricProjections.UTM,
            78.5397
        ),
        (
            SrPoint.from_lat_lon(lat=45.553670, lon=-94.142430),
            5,
            1000,
            MetricProjections.US_NAEA,
            78.5397
        ),
    ]
)
def test_buffer_area(geometry, radius, resolution, metric_projection, area_m):
    """
    Arrange: Create a buffer from an input geometry.
    Act: Calculate the area of the buffer in meters.
    Assert: The area (in meters) matches the expected result.

    :param geometry: the geometry
    :param radius: the buffer radius
    :param resolution: the buffer resolution
    :param metric_projection: the metric projection to use when calculating
        the buffer and the area
    :param area_m: the expected area (in meters)
    """
    buffer = geometry.buffer(
        n=radius,
        metric_projection=metric_projection,
        resolution=resolution
    )
    buffer_area = buffer.area(metric_projection=metric_projection)
    print(round(buffer_area, 3))
    assert round(area_m, 3) == round(buffer_area, 3)
