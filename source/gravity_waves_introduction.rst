Inertia-Gravity Waves
=======================================================

Introduction to inertia gravity waves. We typically use some version of the following equation set;

.. math::
   \begin{align}
   u_t &= \frac{f}{\omega}v - p_x - \frac{\alpha}{\omega}u, \tag{1} \\
   v_t &= -\frac{f}{\omega}u - \frac{\alpha}{\omega}v, \tag{2} \\
   \frac{\omega^2}{N^2}w_t &= b - p_z - \frac{\omega^2}{N^2}\frac{\alpha}{\omega}w, \tag{3} \\
   b_t + w &= Q - \frac{\alpha}{\omega} b, \tag{4} \\
   u_x + w_z &= 0, \tag{5} \\
   w(z=0) &= 0. \tag{6}
   \end{align}

.. toctree::
   :maxdepth: 1

   mountain_valley.rst
   gaussian_forcing.rst
   point_forcing_over_slope.rst
   localized_line_forcing.rst
   land_sea.rst