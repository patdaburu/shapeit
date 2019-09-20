#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 9/11/19 by Pat Daburu
"""
.. currentmodule:: shapeit.geometry.multi
.. moduleauthor:: Pat Daburu <pat@daburu.net>

This module contains multipart geometry objects.
"""
from typing import Mapping, Union
from shapely.geometry import MultiPoint, MultiLineString, MultiPolygon
from shapely.ops import unary_union
from .base import (
    SrGeometry,
    SrPolygon,
    SrGeometry1D,
    SrGeometry2D,
    update_geometry_type_map
)
from ..srs import Sr, WGS_84


class SrMultiPoint(SrGeometry):
    """
    A spatially referenced mutlipoint geometry.
    """
    def __init__(
            self,
            base_geometry: Union[MultiPoint, Mapping],
            sr: Sr = WGS_84
    ):
        super().__init__(base_geometry=base_geometry, sr=sr)

    @property
    def multipoint(self) -> MultiPoint:
        """
        Get the base geometry as a `shapely.geometry.MultiPoint`.
        """
        return self._base_geometry


class SrMultiPolygon(SrGeometry2D):
    """
    A spatially referenced multipolygon geometry.
    """
    def __init__(
            self,
            base_geometry: Union[MultiPolygon, Mapping],
            sr: Sr = WGS_84
    ):
        super().__init__(base_geometry=base_geometry, sr=sr)

    @property
    def multipolygon(self) -> MultiPolygon:
        """
        Get the base geometry as a `shapely.geometry.MultiPolygon`.
        """
        return self._base_geometry

    @property
    def dissolve(self) -> SrPolygon:
        """
        Get a representation of the union of the the polygons.

        :return: the dissolved polygon
        """
        return SrPolygon(
            base_geometry=unary_union(self._base_geometry),
            sr=self._sr
        )


class SrMultiPolyline(SrGeometry1D):
    """
    A spatially referenced polyline geometry.
    """
    def __init__(
            self,
            base_geometry: Union[MultiLineString, Mapping],
            sr: Sr = WGS_84
    ):
        super().__init__(base_geometry=base_geometry, sr=sr)

    @property
    def multilinestring(self) -> MultiLineString:
        """
        Get the base geometry as a `shapely.geometry.Polygon`.
        """
        return self._base_geometry


SrMultiLinestring = (
    SrMultiPolyline
)  #: This is an alias for :py:class:`SrMultiPolyline`


# Update the geometry type map to include the new geometries defined in this
# module.
update_geometry_type_map(MultiPoint, SrMultiPoint)
update_geometry_type_map(MultiPolygon, SrMultiPolygon)
update_geometry_type_map(MultiLineString, SrMultiPolyline)
