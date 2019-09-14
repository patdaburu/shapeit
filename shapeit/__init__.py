#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: shapeit
.. moduleauthor:: Pat Daburu <pat@daburu.net>

It's Shapely with projections and some other conveniences!
"""
from .geometry import SrGeometry, SrPoint, SrPolyline, SrPolygon
from .sr import WGS_84, InvalidSrException
from .version import __version__, __release__
