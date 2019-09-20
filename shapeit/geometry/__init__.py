#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 9/11/19
"""
.. currentmodule:: shapeit.geometry
.. moduleauthor:: Pat Daburu <pat@daburu.net>

This package contains geometry objects and utilities.
"""
from .base import (
    sr_shape,
    SrGeometry,
    SrPoint,
    SrPolygon,
    SrPolyline
)
from .multi import (
    SrMultiPoint,
    SrMultiPolyline,
    SrMultiPolygon
)
