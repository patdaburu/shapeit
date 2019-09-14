.. _examples_wgs84_to_utm:

WGS84 to UTM
============

In this example we'll start with a latitude and a longitude and create a
:py:class:`point <shapeit.geometry.base.SrPoint>` that happens to be in
`UTM zone 15N <https://spatialreference.org/ref/epsg/32615/>`_ (32615).  We'll
then use the :py:func:`as_utm <shapeit.geometry.base.SrGeometry.as_utm>` method
to create the equivalent point in the UTM coordinate system.


.. code-block::

    from shapeit import SrPoint

    # Create a point from a latitude, longitude.
    wgs84 = SrPoint.from_lat_lon(lat=45.553670, lon=-94.142430)

    # Convert it to UTM.
    utm = wgs84.as_utm()

    # What are the coordinates of the UTM point?
    print(f'x={utm.x}, y={utm.y}')

    # What's the SRID of the UTM point's coordinate system.
    print(f"The UTM SRID is: {utm.srid}")

.. code-block:: coq

    x=410830.5412685075, y=5045093.805781859
    The UTM SRID is: 32615

Notice that we didn't have to specify which UTM zone to use.  It's selected
automatically based on the coordinate we supplied.