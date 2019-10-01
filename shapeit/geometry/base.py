#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 9/11/19 by Pat Daburu
"""
.. currentmodule:: geometry
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Geometries start here.
"""
from abc import ABC
import copy
import hashlib
from typing import Any, Dict, Mapping, Union
from shapely.geometry import mapping, LineString, Point, Polygon, shape
from shapely.geometry.base import BaseGeometry, BaseMultipartGeometry
from shapely.ops import transform
from ..measure import convert, meters, Units
from ..srs import (
    by_srid,
    MetricProjections,
    Sr,
    utm,
    transform_fn,
    UnsupportedMetricProjectionException,
    US_NAEA,
    WEB_MERCATOR,
    WGS_84
)
from ..types import pycls, pyfqn
from ..xchg import Exportable


class SrGeometry(Exportable):
    """
    Represents a spatially referenced geometry by combining a
    `Shapely <https://bit.ly/2QovaiU>`_ base geometry with a
    :py:class:`spatial reference <Sr>`.
    """
    __slots__ = ['_base_geometry', '_sr', 'hash_']

    def __init__(
            self,
            base_geometry: Union[BaseGeometry, BaseMultipartGeometry, Mapping],
            sr: Sr = WGS_84
    ):
        # The base geometry we store is the one passed in at the constructor
        # unless the caller passed us a `Mapping` that isn't a base geometry.
        # In that case we'll try to create a geometry from the mapping.
        self._base_geometry = (
            base_geometry if isinstance(
                base_geometry,
                (BaseGeometry, BaseMultipartGeometry)
            )
            else shape(base_geometry)
        )  #: the base (Shapely) geometry
        self._sr = sr  #: the spatial reference (SR)
        # We'll generate the object hash if and when it's requested.
        self.hash_: int or None = None

    @property
    def base_geometry(self) -> Union[BaseGeometry, BaseMultipartGeometry]:
        """
        Get the base geometry.
        """
        return self._base_geometry

    @property
    def sr(self) -> Sr:
        """
        Get the spatial reference.
        """
        return self._sr

    @property
    def srid(self) -> int:
        """
        Get the `SRID <https://bit.ly/2vLtVSY>`_ of the spatial reference (SR).
        """
        return self._sr.srid

    def location(self) -> 'SrPoint':
        """
        Get a single point that best represents the location of this geometry
        as a single point.

        :return: the point
        """
        return SrPoint(
            base_geometry=self.base_geometry.representative_point,
            sr=self._sr
        )

    def mapping(self) -> Mapping[str, Any]:
        """
        Get a GeoJSON-like mapping of the base geometry.

        :return: the mapping
        """
        return mapping(self.base_geometry)

    def as_wgs84(self) -> 'SrGeometry':
        """
        Get this geometry as a WGS84 geometry.

        :return:  an equivalent geometry in the WGS-84 coordinate system (or the
            original object if it is already in the WGS-84 coordinate system)

        .. note::

            If the geometry is already in the WGS84 coordinate system, the
            method may return the original object.
        """
        if self._sr == WGS_84:
            return self
        return self.transform(sr=WGS_84)

    def as_utm(self) -> 'SrGeometry':
        """
        Get this geometry in the regional UTM projection.

        :return:  an equivalent geometry in a UTM coordinate system (or the
            original object if it is already in a UTM coordinate system)

        .. note::

            If the geometry is already in a UTM coordinate system, the method
            may return the original object.
        """
        # If the geometry is in WGS-84...
        if self._sr == WGS_84:
            # ... we can get its representative point (which should be defined
            # as latitude and longitude) directly.
            rp: Point = self.base_geometry.representative_point()
        else:
            # Otherwise, we need to transform it to WGS-84...
            wgs84_geom = self.transform(sr=WGS_84)
            # ...so that we can get a representative point defined by a
            # latitude and a longitude.
            rp: Point = wgs84_geom.base_geometry.representative_point()
        # Get the UTM zone for the latitude and longitude.
        utm_sr = utm(lat=rp.y, lon=rp.x)
        # If the UTM zone matches this geometry's spatial reference (SR)...
        if utm_sr == self._sr:
            return self
        # Transform this geometry's base geometry to the UTM zone.
        return self.transform(sr=utm_sr)

    def as_usm(self) -> 'SrGeometry':
        """
        Get this geometry in the
        `US National Atlas <https://georepository.com/crs_2163/US-National-Atlas-Equal-Area.html>`_
        coordinate system.

        :return:  an equivalent geometry in a US National Atlas coordinate
            system (or the original object if it is already in the US National
            Atlas coordinate system)

        .. note::

            If the geometry is already in the US National Atlas coordinate
            system, the method may return the original object.
        """
        # If the geometry is in already in US National Atlas...
        if self._sr == US_NAEA:
            # ...there's nothing more to do.
            return self
        # Otherwise, just transform it.
        return self.transform(sr=US_NAEA)

    def as_wm(self) -> 'SrGeometry':
        """
        Get this geometry in the
        `Web Mercator <https://en.wikipedia.org/wiki/Web_Mercator_projection>`_
        coordinate system.

        :return:  an equivalent geometry in the web mercator coordinate system
            (or the original object if it is already in web mercator)

        .. note::

            If the geometry is already in the US National Atlas coordinate
            system, the method may return the original object.
        """
        # If the geometry is in already in US National Atlas...
        if self._sr == WEB_MERCATOR:
            # ...there's nothing more to do.
            return self
        # Otherwise, just transform it.
        return self.transform(sr=WEB_MERCATOR)

    def as_metric(
            self,
            metric_projection: MetricProjections = MetricProjections.US_NAEA
    ):
        """
        Get this geometry in one of the defined metric projections.

        :param metric_projection: the preferred type of metric coordinate
            system
        :return: the geometry in one of the defined projections
        :raises UnsupportedMetricProjectionException: if the `metric_projection`
            argument is not supported
        """
        if metric_projection == MetricProjections.US_NAEA:
            return self.as_usm()
        if metric_projection == MetricProjections.UTM:
            return self.as_utm()
        elif metric_projection == MetricProjections.WEB_MERCATOR:
            return self.as_wm()
        # This shouldn't happen unless we introduce a new standard metric
        # projection without updating this method, but...
        raise UnsupportedMetricProjectionException(metric_projection.name)

    def transform(self, sr: Sr or int) -> 'SrGeometry':
        """
        Transform this geometry to

        :param sr: the target spatial reference
        :return: an :py:class:`SrGeometry` in the target spatial reference
        """
        # Let's get the spatial reference (`Sr`): the caller may have given
        # us a ready-made one, but may also have just indicated the SRID.
        _sr = (
            sr if isinstance(sr, Sr)
            else by_srid(srid=sr)
        )
        # If the target `Sr` is this geometry's spatial reference, just return
        # this geometry.
        if _sr == self._sr:
            return self
        # Get the transformation function.
        _transform_fn = transform_fn(from_=self._sr, to=_sr)
        # Perform the transformation to get the new base geometry.
        transformed_geometry = transform(_transform_fn, self._base_geometry)
        # Create the new `SrGeometry` using the transformed base geometry and
        # the spatial reference the caller supplied.
        return sr_shape(
            base_geometry=transformed_geometry,
            sr=_sr
        )

    def buffer(
            self,
            n: int or float,
            units: Units = Units.METERS,
            resolution: int = 64,
            metric_projection: MetricProjections = MetricProjections.UTM
    ) -> 'SrPolygon':
        """
        Buffer the geometry by `n` meters.

        :param n: the radius
        :param units: the radius distance units
        :param resolution: the number of segments used to approximate a quarter
            circle around a point
        :param metric_projection: the preferred metric projection to use
        :return: the buffered geometry
        """
        # Get the geometry in a UTM coordinate system.
        base_utm = self.as_metric(metric_projection)
        # Buffer the base geometry.
        base_utm_buf = base_utm.base_geometry.buffer(
            distance=meters(n, units),
            resolution=resolution
        )
        # Create a new `SrGeometry` with the buffered base geometry and the
        # UTM spatial reference.
        sr_geom_buf = SrPolygon(
            base_geometry=base_utm_buf,
            sr=base_utm.sr
        )
        # Transform the buffered polygon to the original coordinate system
        # and return it.
        return sr_geom_buf.transform(self._sr)

    def export(self) -> Mapping[str, Any]:
        """
        Export the instance as a mapping of simple types.

        :return: the mapping
        """
        return {
            '__type__': pyfqn(self),
            'base_geometry': mapping(self._base_geometry),
            'sr': self._sr._asdict()
        }

    @classmethod
    def load(cls, data: Mapping[str, Any]) -> 'SrGeometry' or None:
        """
        Create an instance from a mapping.

        :param data: the data
        :return: the instance
        """
        # If we didn't receive any data...
        if not data:
            # ...then the answer is nothing.
            return None
        try:
            _cls = pycls(data['__type__'])
        except KeyError:
            _cls = cls

        return _cls(
            **{
                'base_geometry': shape(data.get('base_geometry')),
                'sr': Sr(**data.get('sr'))
            }
        )

    def __hash__(self):
        # NOTE TO THE FUTURE:  We could probably implement a faster hashing
        # algorithm.

        # If we haven't generated the hash yet...
        if self.hash_ is None:
            # ...do so now.
            sha = hashlib.sha3_512(  # pylint: disable=no-member
                str(self.export()).encode('UTF-8')
            )
            self.hash_ = int(sha.hexdigest(), 16)
        # Return the generated hash value.
        return self.hash_

    def __copy__(self):
        return self.__class__(
            base_geometry=copy.deepcopy(self._base_geometry),
            sr=self._sr
        )

    def __getstate__(self):
        return {
            '_base_geometry': mapping(self._base_geometry),
            '_sr': self._sr
        }

    def __setstate__(self, state):
        self._base_geometry = shape(state.get('_base_geometry'))
        self._sr = state.get('_sr')

    def __eq__(self, other):
        # If the other object is None (or empty), the equality check fails.
        if not other:
            return False
        try:
            # If the spatial references don't match...
            if not self._sr == getattr(other, '_sr'):
                return False  # ... no match!
            # If this object has no base geometry...
            if not self._base_geometry:
                # ...it's only equal if the other object also lacks a base
                # geometry.
                return not getattr(other, '_base_geometry')
            # Otherwise, compare this instance's base geometry to the other's
            # as the final equality test.
            return self._base_geometry.equals(getattr(other, '_base_geometry'))
        except AttributeError:
            # Missing attributes are a clear sign that the other object doesn't
            # equal this one.
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"base_geometry={repr(self.mapping())}, "
            f"sr={repr(self._sr)})"
        )

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"base_geometry={self.mapping()}, "
            f"sr={repr(self._sr)}"
            f")"
        )


class SrGeometry1D(SrGeometry, ABC):
    """
    Extend this class to implement `SrGeometry` subclasses that represent
    1-dimensional geometries.

    .. seealso::

        :py:class:`SrPolyline`
    """

    def length(
            self,
            units: Units = Units.METERS,
            metric_projection: MetricProjections = MetricProjections.UTM
    ) -> float:
        """
        Get the length of the polyline in the specified units.

        :param units: the units in which the length should be expressed
        :param metric_projection: the preferred metric projection to use
        :return: the length
        """
        # Get the geometry in a UTM coordinate system.
        _utm = self.as_metric(metric_projection)
        # Now that it's in a coordinate system measured in meters, we can
        # return the length with confidence.
        return convert(
            n=_utm.base_geometry.length,
            units=Units.METERS,
            to=units
        )


class SrGeometry2D(SrGeometry, ABC):
    """
    Extend this class to implement `SrGeometry` subclasses that represent
    2-dimensional geometries.

    .. seealso::

        :py:class:`SrPolygon`
    """
    def area(
            self,
            units: Units = Units.METERS
    ) -> float:
        """
        Get the area of the polygon in the specified units (squared).

        :param units: the units in which the area should be expressed
        :return: the area
        """
        # Get the geometry in a UTM coordinate system.
        _utm = self.as_utm()
        # Now that it's in a coordinate system measured in meters, we can
        # return the area with confidence.
        return convert(
            n=_utm.base_geometry.area,
            units=Units.METERS,
            to=units
        )


class SrPoint(SrGeometry):
    """
    A spatially referenced point geometry.
    """
    def __init__(
            self,
            base_geometry: Union[Point, Mapping],
            sr: Sr = WGS_84
    ):
        super().__init__(base_geometry=base_geometry, sr=sr)

    @property
    def point(self) -> Point:
        """
        Get the base geometry as a `shapely.geometry.Point`.
        """
        return self._base_geometry

    @property
    def x(self) -> float:
        """
        Get the X coordinate.
        """
        return self._base_geometry.x

    @property
    def y(self) -> float:
        """
        Get the Y coordinate.
        """
        return self._base_geometry.y

    def location(self) -> 'SrPoint':
        """
        Get a single point that best represents the location of this geometry
        as a single point.

        :return: the current instance
        """
        # Return the point in the center of the line.
        return self

    @classmethod
    def from_lat_lon(cls, lat: float, lon: float):
        """
        Create a point from a latitude and longitude.

        :param lat: the latitude
        :param lon: the longitude
        :return: the point

        .. seealso::

            :py:attr:`shapeit.sr.WGS_84`
        """
        base_geometry = Point(lon, lat)
        return SrPoint(
            base_geometry=base_geometry,
            sr=WGS_84
        )

    @classmethod
    def from_coords(
            cls,
            x: float,
            y: float,
            sr: int or Sr
    ) -> 'SrPoint':
        """
        Create a point from a set of coordinates and a spatial reference.

        :param x: the X coordinate
        :param y: the Y coordinate
        :param sr: the spatial reference ID (SRID) or an `Sr` that
            represents the spatial reference
        :return: the point
        """
        # Create the base geometry.
        base_geometry = Point(x, y)
        # Create and return the point.
        return SrPoint(
            base_geometry=base_geometry,
            sr=sr if isinstance(sr, Sr) else Sr(srid=sr)
        )


class SrPolygon(SrGeometry2D):
    """
    A spatially referenced polygon geometry.
    """
    def __init__(
            self,
            base_geometry: Union[Polygon, Mapping],
            sr: Sr = WGS_84
    ):
        super().__init__(base_geometry=base_geometry, sr=sr)

    @property
    def polygon(self) -> Polygon:
        """
        Get the base geometry as a `shapely.geometry.Polygon`.
        """
        return self._base_geometry


class SrPolyline(SrGeometry1D):
    """
    A spatially referenced polyline geometry.
    """
    def __init__(
            self,
            base_geometry: Union[LineString, Mapping],
            sr: Sr = WGS_84
    ):
        super().__init__(base_geometry=base_geometry, sr=sr)

    @property
    def linestring(self) -> LineString:
        """
        Get the base geometry as a `shapely.geometry.LineString`.
        """
        return self._base_geometry

    def location(self) -> 'SrPoint':
        """
        Get a single point that best represents the location of this geometry
        as a single point.

        :return: the point
        """
        # Return the point in the center of the line.
        return SrPoint(
            base_geometry=self.base_geometry.interpolate(0.5, normalized=True),
            sr=self._sr
        )


SrLinestring = SrPolyline  #: This is an alias for :py:class:`SrPolyline`

#: a mapping of Shapely geometry types to SrGeometry types
_geometry_type_map: Dict[type, type] = {
    Point: SrPoint,
    LineString: SrPolyline,
    Polygon: SrPolygon
}


def update_geometry_type_map(shapely: type, shapeit: type):
    """
    Update the geometry type map.

    :param shapely: the `Shapely` `BaseGeometry` type
    :param shapeit: the `shapeit` :py:class:`SrGeometry` type
    """
    _geometry_type_map[shapely] = shapeit


def sr_shape(
        base_geometry: Union[BaseGeometry, BaseMultipartGeometry, Mapping],
        sr: Sr or int = WGS_84
) -> Union[SrGeometry, SrPoint, SrPolyline, SrPolygon]:
    """
    Create a :py:class:`SrGeometry` from a `Shapely` geometry (or mapping).

    :param base_geometry: the base geometry (or mapping)
    :param sr: the spatial reference
    :return: the :py:class:`SrGeometry`

    .. note::

        The returned depends on the type of `Shapely` base geometry the
        `base_geometry` parameter describes.
    """
    # Create the Shapely base geometry.
    _base_geometry = (
        base_geometry if isinstance(
            base_geometry,
            (BaseGeometry, BaseMultipartGeometry)
        )
        else shape(base_geometry)
    )
    # Figure out which class we need to instantiate.
    sr_geom_cls = _geometry_type_map.get(
        type(_base_geometry), SrGeometry
    )
    # Instantiate the class.
    return sr_geom_cls(
        base_geometry=_base_geometry,
        sr=sr if isinstance(sr, Sr) else by_srid(sr)
    )
