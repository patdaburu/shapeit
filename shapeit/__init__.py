#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: shapeit
.. moduleauthor:: Pat Daburu <pat@daburu.net>

It's Shapely with projections and some other conveniences!
"""
from .geometry import (
    sr_shape,
    SrGeometry,
    SrPoint,
    SrPolyline,
    SrPolygon,
    SrMultiPoint,
    SrMultiPolyline,
    SrMultiPolygon
)
from .srs import (
    InvalidSrException,
    MetricProjections,
    UnsupportedMetricProjectionException,
    WEB_MERCATOR,
    WGS_84
)
from .version import __version__, __release__
