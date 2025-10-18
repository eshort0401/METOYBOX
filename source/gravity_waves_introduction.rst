Inertia-Gravity Waves
=======================================================

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

Note :math:`Q` represents a forcing on the Buoyancy tendency. For instance, Rotunno (1983), `Qian et al. (2009)`_, and many subsequent papers have considered the forcing 

.. math::
   Q = \frac{Q_0}{\pi}\left(\frac{\pi}{2}+\arctan\left(\frac{x_*}{L}\right)\right)\exp\left(-\frac{z_*}{H}\right)\cos(\omega t_*),
   
which emulates the heating/cooling of a land-surface :math:`x>0` as compared to an ocean surface :math:`x<0`, where :math:`L` and :math:`H` are horizontal and vertical length scales, respectively, and :math:`\omega` is the diurnal frequency. 

Next we scale variables to remove units. Such scaling is called nondimensionalization. An immediate reason for doing this is that units can be mathematically inconvenient; for instance, what are the units of :math:`\ln(10 \text{ m})`? Better to scale out the units at the start to avoid such ambiguity. Another reason is that nondimensionalization typically `reduces the parameter space`_, and reveals how the solution scales with different parameters. For the models in this section we use the following scalings from `Qian et al. (2009)`_;

.. math::
   \begin{align}
   \begin{split}
   &x^*=\frac{NH}{\omega}x, \quad y^*=\frac{NH}{\omega}y, \quad z^*=Hz,\quad t^*=\frac{t}{\omega}, \\
   &Q^*=Q_0Q,\quad u^*=\frac{Q_0}{N\omega}u, \quad v^*=\frac{Q_0}{N\omega}v, \quad w^* = \frac{Q_0}{N^2}w, \\
   &b^* = \frac{Q_0}{\omega} b,\quad p^*= \frac{Q_0H}{\omega}p,
   \end{split}
   \end{align}

where :math:`H` is a representative height scale, :math:`\omega` a representative frequency, and :math:`Q_0` a representative amplitude of the forcing :math:`Q`. These scales are not particularly important; they are simply chosen to ensure the numbers in our solution are not prohibitively small or large. Note these scales can often be chosen directly from the forcing function. With the land-sea breeze :math:`Q` given above :math:`\omega=\frac{2\pi}{24\cdot 3600}` is the diurnal frequency, but in general :math:`\omega` can be any frequency of interest. Substituting the above expressions into our governing equations and simplifying we get

.. math::
   \begin{align}
   u_t &= \frac{f}{\omega}v - p_x - \frac{\alpha}{\omega}u, \\
   v_t &= -\frac{f}{\omega}u - \frac{\alpha}{\omega}v, \\
   \frac{\omega^2}{N^2}w_t &= b - p_z - \frac{\omega^2}{N^2}\frac{\alpha}{\omega}w, \\
   b_t + w &= Q - \frac{\alpha}{\omega} b, \\
   u_x + w_z &= 0, \\
   w(z=0) &= 0.
   \end{align}

Note that for some of the models we will consider :math:`\omega` will be the diurnal frequency :math:`\frac{2\pi}{24\cdot 3600}`, and hence :math:`\frac{\omega^2}{N^2}` will be tiny and can be neglected. Wave solutions for which :math:`\frac{\omega^2}{N^2}`

.. toctree::
   :maxdepth: 1

   slope_breeze.rst
   gaussian_forcing.rst
   point_forcing_over_slope.rst
   localized_line_forcing.rst
   land_sea.rst

.. _Boussinesq/shallow-anelastic: https://doi.org/10.1175/1520-0469(1962)019<0173:SAODAS>2.0.CO;2

.. _reduces the parameter space: https://en.wikipedia.org/wiki/Buckingham_%CF%80_theorem

.. _Qian et al. (2009): https://doi.org/10.1175/2008JAS2851.1