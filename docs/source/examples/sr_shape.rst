.. _examples_sr_shape:

Making Shapes: ``sr_shape``
===========================

If you have a
`Shapely geometry <https://shapely.readthedocs.io/en/stable/manual.html#geometric-objects>`_ you can
use the :py:func:`sr_shape <shapeit.geometry.base.sr_shape>` function to convert it into an
:py:class:`SrGeometry <shapeit.geometry.base.SrGeometry>` instance.

The function will determine the best `SrGeometry` type by inspecting the Shapely base geometry.

.. code-block:: python

    from shapely.geometry import LineString, Polygon
    from shapeit import sr_shape

    geometry1 = sr_shape(
        base_geometry=LineString([(2, 0), (2, 4), (3, 4)])
    )

    geometry2 = sr_shape(
        base_geometry=Polygon([(0, 0), (1, 1), (1, 0)]),
        sr=32615
    )

    print(f"geometry1 is a(n) {type(geometry1).__name__}.")
    print(f"The SRID is {geometry1.srid}.")

    print(f"geometry2 is a(n) {type(geometry2).__name__}.")
    print(f"The SRID is {geometry2.srid}.")

.. seealso::

    * :py:class:`SrPoint <shapeit.geometry.base.SrPoint>`
    * :py:class:`SrMultiPoint <shapeit.geometry.multi.SrMultiPoint>`
    * :py:class:`SrPolyline <shapeit.geometry.base.SrPolyline>`
    * :py:class:`SrMultiPolyline <shapeit.geometry.multi.SrMultiPolyline>`
    * :py:class:`SrPolygon <shapeit.geometry.base.SrPolygon>`
    * :py:class:`SrMultiPolygon <shapeit.geometry.multi.SrMultiPolygon>`