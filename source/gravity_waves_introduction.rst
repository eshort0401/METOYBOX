Inertia-Gravity Waves
=======================================================

Introduction
-------------------------
On this page we introduce a class of linear models originating from the work of `Rotunno (1983)`_. We can often solve these models purely analytically, sometimes discovering interesting connections between the maths, logic and physics. We will use the original `Rotunno (1983)`_ model to contextualize the ideas presented in this introduction; further details on the `Rotunno (1983)`_ model itself can be found on its dedicated page :doc:`land_sea`.

Governing equations
----------------------------
We first linearize the governing equations and make the `Boussinesq/shallow-anelastic`_ and :math:`f`-plane approximations, using :math:`*` to denote dimensional variables;

.. math::
   \begin{align}
   \frac{\partial u_*}{\partial t_*} &= fv_* - \frac{\partial p_*}{\partial x_*} - \alpha u_*, \\
   \frac{\partial v_*}{\partial t_*} &= -fu_* - \alpha v_*, \\
   \frac{\partial w_*}{\partial t_*} &= b_* - \frac{\partial p_*}{\partial z_*} - \alpha w_*, \\
   \frac{\partial b_*}{\partial t_*} + N^2 w_* &= Q_* - \alpha b_*, \\
   \frac{\partial u_*}{\partial x_*} + \frac{\partial w_*}{\partial z_*} &= 0, \\
   w_*(z_*=0) &= 0. 
   \end{align}

The function :math:`Q_*` represents a forcing on the buoyancy tendency we might loosely call "heating". `Rotunno (1983)`_, `Qian et al. (2009)`_, and many subsequent papers considered

.. math::
   Q = \frac{Q_0}{\pi}\left(\frac{\pi}{2}+\arctan\left(\frac{x_*}{L}\right)\right)\exp\left(-\frac{z_*}{H}\right)\cos(\omega t_*),
   
which emulates the heating/cooling of a land-surface :math:`x>0` as compared to an ocean surface :math:`x<0`, where :math:`L` and :math:`H` are horizontal and vertical length scales, respectively, and :math:`\omega` is the diurnal frequency. The interactive model below provides a visualization of this choice of :math:`Q`; in our interactive figures we omit the :math:`*` subscripts for the dimensional coordinates, as the coordinate type is clear from the radio button.

.. raw:: html
   :file: ./_static/land_sea_intro.html

You should play with the :math:`t`, :math:`Q_0`, :math:`H` and :math:`L` sliders to see how the forcing :math:`Q` changes. If you switch on the quiver plot you will be able to see the winds overlaid on :math:`Q`. You can also switch the shading to one of the other variables, e.g. :math:`u`, to study the response in more detail. If the interactive figure is laggy, try using Chrome!

Non-Dimensionalization
-------------------------
Next we scale variables to remove units. Such scaling is called non-dimensionalization. An immediate reason to non-dimensionalize is that units are often mathematically inconvenient; for instance, what are the units of :math:`\ln(10 \text{ m})`? Another reason to non-dimensionalize is to `reduce the number of independent variables`_ in our models. Yet another reason to non-dimensionalize is to ensure we can always choose axis limits in our plots so that the interesting part of the model is visible. For the models in this section we use the following scalings from `Qian et al. (2009)`_;

.. math::
   \begin{align}
   \begin{split}
   &x^*=\frac{NH}{\omega}x, \quad y^*=\frac{NH}{\omega}y, \quad z^*=Hz,\quad t^*=\frac{t}{\omega}, \\
   &Q^*=Q_0Q,\quad u^*=\frac{Q_0}{N\omega}u, \quad v^*=\frac{Q_0}{N\omega}v, \quad w^* = \frac{Q_0}{N^2}w, \\
   &b^* = \frac{Q_0}{\omega} b,\quad p^*= \frac{Q_0H}{\omega}p,
   \end{split}
   \end{align}

where :math:`H` is a representative height scale, :math:`\omega` a representative frequency, and :math:`Q_0` a representative amplitude of the forcing :math:`Q`. These scales can often be inferred from the forcing function :math:`Q`. Note with the land-sea breeze :math:`Q` given above, :math:`\omega=\frac{2\pi}{24\cdot 3600}` is the diurnal frequency. In general however, :math:`\omega` can be any representative frequency appropriate for the given problem.

Substituting the above scaling expressions into our governing equations and simplifying we get

.. math::
   \begin{align}
   u_t &= \frac{f}{\omega}v - p_x - \frac{\alpha}{\omega}u, \\
   v_t &= -\frac{f}{\omega}u - \frac{\alpha}{\omega}v, \\
   \frac{\omega^2}{N^2}w_t &= b - p_z - \frac{\omega^2}{N^2}\frac{\alpha}{\omega}w, \\
   b_t + w &= Q - \frac{\alpha}{\omega} b, \\
   u_x + w_z &= 0, \\
   w(z=0) &= 0.
   \end{align}

The `Rotunno (1983)`_ :math:`Q` function becomes

.. math::
   Q = \frac{1}{\pi}\left(\frac{\pi}{2}+\arctan\left(\frac{x}{\mathcal{L}}\right)\right)\exp\left(-z\right)\cos(t),

where :math:`\mathcal{L} = \frac{\omega}{NH}L` is the non-dimensional horizontal length scale. 

Scrolling back up to the interactive figure (or opening in other window), you should click the radio button to switch to non-dimensional coordinates. Note in our interactive figures we write the horizontal length scale simply as :math:`L` for both dimensional and non-dimensional coordinates, as javascript struggles with calligraphic math symbols, and the meaning of :math:`L` is clear from the context. Notice how the number of sliders decreases by two when using non-dimensional coordinates compared to dimensional coordinates. As noted above, non-dimensionalization lets us reduce the number of independent variables, or in fancy language, "reduce the dimension of the parameter space" of our models. Switching back to dimensional coordinates, notice how variables like :math:`N` don't change the core structure of the response, but do scale the tick labels on the :math:`x` axis, ensuring our figure always contains the interesting part of the solution.

Hydrostatic Waves
----------------------------
When :math:`\omega = \frac{2\pi}{24\cdot 3600}` is the diurnal frequency, :math:`\frac{\omega^2}{N^2}` is tiny, and terms containing this factor can be neglected. Wave solutions for which :math:`\frac{\omega^2}{N^2} \approx 0` are, somewhat confusingly, called hydrostatic waves. The adjective "hydrostatic" reflects :math:`\frac{\omega^2}{N^2} \approx 0 \Rightarrow b \approx p_z`, i.e. that buoyancy forces are approximately balanced by vertical pressure gradient forces. In this context the balance is only approximate, and hence does not imply :math:`w=0`. Indeed, as we will see later, vertical velocities are essential to the core dynamics of gravity waves. The concept of "hydrostatic waves" is thus distinct from the usual "hydrostatic balance" condition :math:`\frac{\partial p}{\partial z} = -\rho g` we encounter in synoptic meteorology, which does imply :math:`w=0`.

In the land-sea breeze model above, :math:`\omega` is indeed the diurnal frequency, and so the model is mostly unresponsive to :math:`\frac{N}{\omega}`, except for the very smallest values. Later we will consider models that are responsive to :math:`\frac{N}{\omega}`. Switching back to dimensional coordinates however, we see that varying :math:`N` changes the tick labels on the :math:`x` axis, in accordance with the scalings given above. 

Solution Method
------------------------------
Forthcoming.

Models
-----------------

.. toctree::
   :maxdepth: 1

   land_sea.rst
   gaussian_forcing.rst
   localized_line_forcing.rst
   slope_breeze.rst
   point_forcing_over_slope.rst
   
.. _Boussinesq/shallow-anelastic: https://doi.org/10.1175/1520-0469(1962)019<0173:SAODAS>2.0.CO;2

.. _reduce the number of independent variables: https://en.wikipedia.org/wiki/Buckingham_%CF%80_theorem

.. _Qian et al. (2009): https://doi.org/10.1175/2008JAS2851.1

.. _Rotunno (1983): https://doi.org/10.1175/1520-0469(1983)040<1999:OTLTOT>2.0.CO;2