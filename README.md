# shapeit

[Shapely](https://shapely.readthedocs.io/en/stable/manual.html) is great for working with geometries, but if you're dealing with Geographic Information Systems ([GIS](https://www.nationalgeographic.org/encyclopedia/geographic-information-system-gis/)) there
are times when you really need your geometries to have some awareness of [spatial reference](https://en.wikipedia.org/wiki/Spatial_reference_system).  This project seeks to combine `Shapely` with [pyproj](https://pypi.org/project/pyproj/) and some other conveniences to make working with geometries across spatial references easy and fun!

## Project Features

* [shapeit](https://readthedocs.org/projects/shapeit/)
* automated unit tests you can run with [pytest](https://docs.pytest.org/en/latest/)
* a [Sphinx](http://www.sphinx-doc.org/en/master/) documentation project

## Getting Started

The project's documentation contains a section to help you
[get started](https://shapeit.readthedocs.io/en/latest/getting_started.html) as a developer or
user of the library.

## Examples

### WGS84 to UTM

In this example we'll start with a latitude and a longitude and create a point that happens to be in
[UTM zone 15N](https://spatialreference.org/ref/epsg/32615/) (32615).  We'll then use the `as_utm` method to create the equivalent point in the UTM coordinate system.

``` python
from shapeit import SrPoint

# Create a point from a latitude, longitude.
wgs84 = SrPoint.from_lat_lon(lat=45.553670, lon=-94.142430)

# Convert it to UTM.
utm = wgs84.as_utm()

# What are the coordinates of the UTM point?
print(f'x={utm.x}, y={utm.y}')

# What's the SRID of the UTM point's coordinate system.
print(f"The UTM SRID is: {utm.srid}")
```

``` sh
x=410830.5412685075, y=5045093.805781859
The UTM SRID is: 32615
```


For more examples and other information, visit the [documentation page](https://shapeit.readthedocs.io/en/latest/).



## Development Prerequisites

If you're going to be working in the code (rather than just using the library), you'll want a few utilities.

* [GNU Make](https://www.gnu.org/software/make/)
* [Pandoc](https://pandoc.org/)

## Resources

Below are some handy resource links.

* [Project Documentation](http://shapeit.readthedocs.io/)
* [Click](http://click.pocoo.org/5/) is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
* [Sphinx](http://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation, written by Geog Brandl and licnsed under the BSD license.
* [pytest](https://docs.pytest.org/en/latest/) helps you write better programs.
* [GNU Make]  is a tool which controls the generation of executables and other non-source files of a program from the program's source files.


## Authors

* **Pat Daburu** - *Initial work* - [github](https://github.com/patdaburu)

See also the list of [contributors](https://github.com/patdaburu/shapeit/contributors) who participated in this project.

## LicenseMIT License

Copyright (c) patdaburu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.