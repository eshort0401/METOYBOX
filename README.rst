Meteorological Toy Box (METOYBOX)
========================================================================

A collection of meteorological (and other) toy/analytic models. Some pedagogic content. Check out the site `here <https://eshort0401.github.io/METOYBOX/>`_. My goal is excite people about math as much as meteorology. The dream would be to build a site with heaps of models to complement textbooks like Vallis (2007). I think having interactive figures and code alongside the maths could be helpful.

Clone the repo in the usual ways. Local build instructions forthcoming. For now, note that to run the site from a local development webserver it is helpful to create a symbolic link to emulate the directory structure used by GitHub pages.

.. code:: shell

    mkdir -p gh-pages-mirror
    cd gh-pages-mirror
    ln -s ../METOYBOX/docs METOYBOX
    python -m http.server 8000