#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 5/7/19 by Pat Daburu
"""
.. currentmodule:: shapeit.sr
.. moduleauthor:: Pat Daburu <pat@daburu.net>

If you're dealing with spatial references (SR), look in here!
"""
from enum import Enum
from functools import partial
import math
from typing import Callable, Dict, NamedTuple, Tuple, Union
import pyproj
from pyproj import Proj
import pyproj.exceptions
from .errors import ShapeitException

#: `pyproj.Proj` instances cached by srid and authority
_proj_cache: Dict[Tuple[int, str], Proj] = {}


class InvalidSrException(ShapeitException):
    """
    Raised in response to attempts to create or use invalid spatial
    references.
    """


class Authorities(Enum):
    """
    Spatial Reference Authorities
    """
    EPSG = 'epsg'  #: European Petroleum Survey Group


class Sr(NamedTuple):
    """
    Represents a spatial reference.
    """
    srid: int  #: the spatial reference identifier
    authority: str = Authorities.EPSG.value  #: the spatial reference authority

    @property
    def proj(self) -> Proj:
        """
        Get a `pyproj.Proj` object that represents this spatial reference
        (SR).
        """
        try:
            return _proj_cache[(self.srid, self.authority)]
        except KeyError:
            try:
                _proj = Proj(init=f'{self.authority}:{self.srid}')
                _proj_cache[(self.srid, self.authority)] = _proj
                return _proj
            except pyproj.exceptions.CRSError as crsex:
                raise InvalidSrException(
                    message=str(crsex),
                    inner=crsex
                )


class LatLon(NamedTuple):
    """
    Represents a latitude/longitude pair.
    """
    lat: float  #: the latitude
    lon: float  #: the longitude


WGS_84 = Sr(
    srid=4326,
    authority=Authorities.EPSG.value
)  #: the WGS-84 spatial reference

#: a mapping of `Sr` objects indexed by srid (`int`) and authority (`str`)
_sr_cache: Dict[Tuple[int, str], Sr] = {}

#: a mapping of transformation functions indexed by the "from" and "to"
#: spatial references (SR)
_transform_fn_cache: Dict[Tuple[Sr, Sr], Callable] = {}


def sr(
        srid: int,
        authority: str or Authorities = Authorities.EPSG
) -> Sr:
    """
    Get a spatial reference (:py:class:`Sr`).

    :param srid: the `SRID <https://bit.ly/2vLtVSY>`_
    :param authority: the authority
    :return: a spatial reference (SR) instance
    """
    _authority = (
        authority.value
        if isinstance(authority, Authorities)
        else authority
    )
    try:
        return _sr_cache[(srid, _authority)]
    except KeyError:
        _sr = Sr(srid=srid, authority=_authority)
        _sr_cache[(srid, _authority)] = _sr
        return _sr


def utm(lat: float, lon: float) -> Sr:
    """
    Get the spatial reference (SR) of the `UTM zone <https://bit.ly/2hxh7JW>`_
    that contains a geographic coordinate.

    :param lat: the latitude
    :param lon: the longitude
    :return: the spatial reference (SR) of the UTM zone
    """
    utm_band = str((math.floor((lon + 180) / 6) % 60) + 1)
    if len(utm_band) == 1:
        utm_band = '0' + utm_band
    if lat >= 0:
        srid = int(f'326{utm_band}')
    else:
        srid = int(f'327{utm_band}')
    return sr(srid=srid, authority=Authorities.EPSG)


def transform_fn(from_: Sr, to: Sr) -> Callable:
    """
    Get a transformation function for a pair of spatial references (SR).

    :param from_: the spatial reference (SR) of the geometry to be transformed
    :param to: the spatial reference (SR) into which the geometry shall be
        transformed
    :return: a transformation function that can be used with the
        `shapely.ops.transform` function
    """
    try:
        return _transform_fn_cache[(from_, to)]
    except KeyError:
        fn = partial(
            pyproj.transform,
            from_.proj,
            to.proj
        )
        _transform_fn_cache[(from_, to)] = fn
        return fn


def by_srid(
        srid: int,
        authority: Union[Authorities, str] = Authorities.EPSG.name,
        validate: bool = True
) -> Sr:
    """
    Get a spatial reference (`Sr`) by its SRID and, optionally, the authority
    (if it isn't an `EPSG <http://www.epsg.org/>`_ spatial reference).

    :param srid: the SRID
    :param authority: the authority *(The default is `epsg`)*
    :param validate: `True` to validate the :py:class:`Sr`
    :return: the SRID
    :raises InvalidProjectionException: if there is no valid projection defined
        for the spatial reference
    """
    _sr = sr(srid=srid, authority=authority)
    # If we're asked to validate the `Sr`...
    if validate:
        # ...make sure there is a valid projection.
        _ = _sr.proj
    return _sr
