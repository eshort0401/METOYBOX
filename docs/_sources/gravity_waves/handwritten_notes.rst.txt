Handwritten Notes
=======================================

.. admonition:: TODO:

    Organize the pages in these files better; currently the introductory steps are duplicated in some of the files, but missing from others. 

Below are links to the handwritten derivations of the models in this section. These notes likely contain typos/mistakes. Forgive me the notes are a bit jumbled up; I will organize them when I get the time.

- The `Heaviside Forcing Notes <../_static/pdfs/gravity_waves/short25_heaviside.pdf>`_ consider a limiting case :math:`L\to 0` of the Rotunno (1983) model, where the :math:`\arctan` coastal region becomes a Heaviside step function. Working through this problem made me realize we can get a full-solution to the Rotunno (1983) problem using :math:`\operatorname{E_i}` functions; i.e. no numerical inverse Fourier transform required! From memory the original argument I gave about branch cuts here is a bit wrong; really we are choosing the appropriate branch cut for :math:`\operatorname{E_i}` so that anti-derivatives are continuous over the domain of integration, and hence the Fundamental Theorem of Calculus can be used to integrate analytically. 

- The `Rotunno (1983) Notes <../_static/pdfs/gravity_waves/short25_rotunno_notes.pdf>`_ extend the above; note the algebra is almost identical to the Heaviside case.

- The `Gaussian Forcing Notes <../_static/pdfs/gravity_waves/short25_gaussian_notes.pdf>`_ provide a solution for a point forcing in space with a Gaussian time dependence. The idea here is to illustrate we can use the same linear analysis from the Rotunno (1983) model to consider more general, non-periodic forcings.

- The `Localized Line Forcing Notes <../_static/pdfs/gravity_waves/short25_localized_line_notes.pdf>`_ try to make the Gaussian point forcing model a bit more realistic, by forcing over a finite-width line rather than at a point. I'm pretty sure this can be further extended to a purely analytic "diamond forcing" type problem using the same branch cut approach as in the Heaviside notes, but this is very hard.

- The `Sloping Terrain Notes <../_static/pdfs/gravity_waves/short25_wave_slope_notes.pdf>`_ explain the coordinate transform idea used to derive the sloped lower boundary models, then derive the models themselves. Note we get a very interesting mid-latitude versus poleward timing difference for the same reasons as in the Rotunno (1983) model; would be very interesting to explore this idea empirically if it hasn't already been done. 

