.. _examples_wgs84_buffer:

WGS84 Buffer in Meters
======================

Sometimes you're working with location data which is often expressed as
latitude and longitude.  Coordinate systems that measure location in these
terms (like the `World Geodetic System (WGS84) <https://bit.ly/2khmqAZ>`_) use
angular measurement, there are many operations such as buffering; or querying
length or area, that are much more natural to perform in terms of linear
measurements (*e.g.* meters).

In this example we'll start with a latitude and a longitude and create a
:py:class:`point <shapeit.geometry.base.SrPoint>`.  Then we'll create a
buffer polygon (an approximate circle around that point).  Even though the
point geometry is in *WGS-84*, we'll define the
:py:class:`buffer <shapeit.geometry.base.SrGeometry.buffer>`  radius in meters.
The :py:class:`polygon <shapeit.geometry.base.SrPolygon>` buffer will be defined
in the same coordinate system as the buffer (*WGS-84*) but we'll be able to
query its :py:class:`area <shapeit.geometry.base.SrGeometry.buffer>` in terms
of *meters*.

.. code-block:: python

    from shapeit import SrPoint
    from shapeit.measure import Units

    # Create a point from a latitude-longitude pair.
    wgs84 = SrPoint.from_lat_lon(lat=45.553670, lon=-94.142430)

    # We'll create a high `resolution` buffer so we can get a close
    # approximation of the area.
    buffer = wgs84.buffer(5, Units.METERS, resolution=1000)

    # The buffer is still in WGS-84.
    print(f"The buffer's SRID is: {buffer.srid}")

    # The equation for the area of a circle tells us that the buffer's
    # area should be approximately 78.54 meters.
    print(f"The buffer area is: {buffer.area(units=Units.METERS)}")

.. code-block:: coq

    The buffer's SRID is: 4326
    The buffer area is: 78.53978404108517
