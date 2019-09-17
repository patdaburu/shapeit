#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 9/11/19 by Pat Daburu
"""
.. currentmodule:: shapeit.geometry.multi
.. moduleauthor:: Pat Daburu <pat@daburu.net>

This module contains multipart geometry objects.
"""
from typing import Any, Dict, Mapping, Union
from shapely.geometry import MultiPoint, MultiLineString, MultiPolygon
from shapely.geometry.base import BaseGeometry, BaseMultipartGeometry
from .base import SrGeometry1D, SrGeometry2D
from ..measure import convert, Units
from ..sr import Sr, WGS_84


class SrMultiPolygon(SrGeometry2D):
    """
    A spatially referenced multipolygon geometry.
    """
    def __init__(
            self,
            base_geometry: Union[MultiPolygon, Mapping],
            sr_: Sr = WGS_84
    ):
        super().__init__(base_geometry=base_geometry, sr_=sr_)

    @property
    def multipolygon(self) -> MultiPolygon:
        """
        Get the base geometry as a `shapely.geometry.MultiPolygon`.
        """
        return self._base_geometry


class SrMultiPolyline(SrGeometry1D):
    """
    A spatially referenced polyline geometry.
    """
    def __init__(
            self,
            base_geometry: Union[MultiLineString, Mapping],
            sr_: Sr = WGS_84
    ):
        super().__init__(base_geometry=base_geometry, sr_=sr_)

    @property
    def multilinestring(self) -> MultiLineString:
        """
        Get the base geometry as a `shapely.geometry.Polygon`.
        """
        return self._base_geometry


SrMultiLinestring = (
    SrMultiPolyline
)  #: This is an alias for :py:class:`SrMultiPolyline`
