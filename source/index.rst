Meteorological Toybox
=======================================

Welcome to the Meteorological Toybox, a place to explore highly idealized "toy" models of atmospheric phenomena. Why toy models? There are perhaps no longer any compelling scientific reasons. Neural net (artificial intelligence) based models, containing little to no explicit physics, are now outperforming the traditionally derived models of our forebears. Indeed, one might argue the models comprising this site were out-of-date by the mid 80s, when direct, numerical integration of the atmosphere's governing equations became computationally feasible. But I still find toy models compelling.

Toy models can usually be contained almost entirely in a single human mind, creating a - perhaps illusory - sense of mastery, comprehension and control. Such comprehension reveals connections between the physics, math and logic, exposing novel hypotheses not accessible any other way. Of course, the validity of any such hypotheses must ultimately be decided by physical experiment, and the analytic and empirical scientific traditions are often in tension. In meteorology, this dance underlies our understanding of heatwaves, fronts, land-sea breezes, thunderstorms, climate processes, and so forth.

Of course, individual motives for pursuing toy models may have little to do with advancing science or helping people. My own motives are unapologetically banal. I enjoy chasing the dragon through pages and pages of second year engineering algebra. I like tricking people into thinking I'm smart by filling whiteboards with math. I love the rush of seeing disparate topics click together in surprising ways. Most of all, I love how the creative discipline of formal thought orders and structures my mind, providing brief respite from internalized traumatic Cronenberg chaos.

This site thus emphasizes the styles of argument, mathematical techniques and aesthetic presentation of toy models, rather than their practical value. I hope that, at the very least, the site will serve as an interesting museum. The models are coded up in Python, and presented interactively in your browser using `PyScript`_ and JavaScript. I used artificial intelligence to help me learn JavaScript quickly; everything else is Nimbin hippy organic intelligence. Have fun!

.. toctree::
    :maxdepth: 2

    foundations/index.rst
    gravity_waves/index.rst

.. _PyScript: https://pyscript.net

.. warning::

    For some reason the models are laggy in Firefox. Other browsers seem fine.