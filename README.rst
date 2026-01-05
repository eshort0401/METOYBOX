Meteorological Toy Box (METOYBOX)
===============================================================

A collection of meteorological (and other) toy/analytic models. Some pedagogic content.

To access the site from a local webserver it is helpful to create a symbolic link to emulate the structure used by GitHub pages.
```shell
mkdir -p gh-pages-mirror
cd gh-pages-mirror
ln -s ../METOYBOX/docs METOYBOX
python -m http.server 8000
```