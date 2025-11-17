Inertia-Gravity Waves
=======================================================

Introduction
--------------------------------------------
Here we present models that feature inertia-gravity wave dynamics. Most of our models are derived from the work of `Rotunno (1983)`_. We can often solve these models purely analytically, sometimes discovering interesting connections between the maths, logic and physics. On this page, we use the original `Rotunno (1983)`_ model to introduce some key ideas; further details on the `Rotunno (1983)`_ model itself can be found on the :doc:`land_sea` page.

Governing equations
---------------------------------------
We first linearize the governing equations and make the `Boussinesq/shallow-anelastic`_ and :math:`f`-plane approximations. The symbol :math:`*` indicates our variables our "dimensional", i.e. they have physical units. Below we introduce the corresponding unit-less "non-dimensional" variables, which simplify the maths.

.. admonition:: Dimensional Governing Equations

    .. math:: 
        \begin{align}
        \frac{\partial u_*}{\partial t_*} &= fv_* - \frac{\partial p_*}{\partial x_*} - \alpha u_*, \label{u_mom_dim} \\
        \frac{\partial v_*}{\partial t_*} &= -fu_* - \alpha v_*, \label{v_mom_dim} \\
        \frac{\partial w_*}{\partial t_*} &= b_* - \frac{\partial p_*}{\partial z_*} - \alpha w_*, \label{w_mom_dim} \\
        \frac{\partial b_*}{\partial t_*} + N^2 w_* &= Q_* - \alpha b_*, \label{b_dim} \\
        \frac{\partial u_*}{\partial x_*} + \frac{\partial w_*}{\partial z_*} &= 0, \label{cont_dim} \\
        w_*(z_*=0) &= 0. \label{boundary_dim}
        \end{align}
    
The function :math:`Q_*` represents a forcing on the buoyancy tendency we might loosely call "heating". `Rotunno (1983)`_, `Qian et al. (2009)`_, and many subsequent papers consider

.. math::
    \begin{equation}
    Q_* = \frac{Q_0}{\pi}\left(\frac{\pi}{2}+\arctan\left(\frac{x_*}{L}\right)\right)\exp\left(-\frac{z_*}{H}\right)\cos(\omega t_*),
    \label{Q_sea_breeze_dim}
    \end{equation}
    
   
which emulates the heating/cooling of a land-surface :math:`x>0` as compared to an ocean surface :math:`x<0`, where :math:`L` and :math:`H` are horizontal and vertical length scales, respectively, and :math:`\omega` is the diurnal frequency. The applet below visualizes this choice of :math:`Q_*` [#]_.

.. _igw_intro_applet:

**Rotunno (1983) Applet**

.. raw:: html
    :file: ./_static/land_sea_intro.html

The idea is that we have chosen our coordinates :math:`(x_*, y_*, z_*)` so that :math:`*x_*=0`, :math:`z_*=0` represents a coastline, which extends infinitely far into and out of the screen in the :math:`y_*` direction. The :math:`z_*=0` lower boundary represents land and sea for :math:`x_*>0` and :math:`x_*<0`, respectively; imagine you're at the beach, looking down the coastline, with sand to your right, and water to your left. The land surface changes temperature over the course of the day, but the ocean surface temperature is comparatively constant. You should play with the :math:`t`, :math:`Q_0`, :math:`H` and :math:`L` sliders to see how the forcing :math:`Q_*` changes. Also, with :math:`Q_*` given by :math:`\eqref{Q_sea_breeze_dim}` we can solve :math:`\text{\eqref{u_mom_dim}-\eqref{boundary_dim}}` analytically! Switching on the quiver plot shows the :math:`(u, w)` vectors overlaid on :math:`Q`. You can also change the shading from :math:`Q` to another variable, e.g. :math:`v`. If the applets are laggy in Firefox, abandon computer communism, embrace digital counter-revolution, and try Chrome instead!

.. _non-dim:

Non-Dimensionalization
-------------------------------------
Next we scale variables to remove units, i.e. we non-dimensionalize. One reason to non-dimensionalize is that units are mathematically annoying; what are the units of :math:`\ln(10 \text{ m})`? Another reason to non-dimensionalize is to `reduce the number of independent variables`_ in our models. Yet another reason is to ensure the interesting parts of our models are always visible in our figures as we mess with the parameters!

Here we use the scalings from `Qian et al. (2009)`_;

.. math::
    \begin{align}
    \begin{split}
    &x^*=\frac{NH}{\omega}x, \quad y^*=\frac{NH}{\omega}y, \quad z^*=Hz,\quad t^*=\frac{t}{\omega}, \\
    &Q^*=Q_0Q,\quad u^*=\frac{Q_0}{N\omega}u, \quad v^*=\frac{Q_0}{N\omega}v, \quad w^* = \frac{Q_0}{N^2}w, \\
    &b^* = \frac{Q_0}{\omega} b,\quad p^*= \frac{Q_0H}{\omega}p,
    \end{split}
    \label{scalings}
    \end{align}

where :math:`H` is a representative height scale, :math:`\omega` a representative frequency, and :math:`Q_0` a representative amplitude of the forcing :math:`Q`. These scales can often be inferred from the forcing function :math:`Q`. Note with the land-sea breeze :math:`Q` given above, :math:`\omega=\frac{2\pi}{24\cdot 3600} \text{ s}^{-1}\approx 7.272 \times 10^{-5} \text{ s}^{-1}` is the diurnal frequency. In general however, :math:`\omega` can be any representative frequency appropriate for the given problem.

Substituting the above scaling expressions into our governing equations and simplifying we get

.. admonition:: Non-Dimensional Governing Equations

    .. math::
        \begin{align}
        u_t &= \frac{f}{\omega}v - p_x - \frac{\alpha}{\omega}u, \label{u_mom} \\
        v_t &= -\frac{f}{\omega}u - \frac{\alpha}{\omega}v, \label{v_mom} \\
        \frac{\omega^2}{N^2}w_t &= b - p_z - \frac{\omega^2}{N^2}\frac{\alpha}{\omega}w, \label{w_mom} \\
        b_t + w &= Q - \frac{\alpha}{\omega} b, \label{b} \\
        u_x + w_z &= 0, \label{cont} \\
        w(z=0) &= 0. \label{boundary}
        \end{align}

The `Rotunno (1983)`_ :math:`Q_*` function :math:`\eqref{Q_sea_breeze_dim}` becomes

.. math::
    \begin{equation}
    Q = \frac{1}{\pi}\left(\frac{\pi}{2}+\arctan\left(\frac{x}{\mathcal{L}}\right)\right)\exp\left(-z\right)\cos(t), \label{Q_sea_breeze}
    \end{equation}

where :math:`\mathcal{L} = \frac{\omega}{NH}L` is the non-dimensional horizontal length scale. [#]_

Scroll back up to the :ref:`applet <igw_intro_applet>` (or open it in another window) and click the radio button to switch to non-dimensional coordinates. Notice the number of sliders decreases by two. As noted above, non-dimensionalization typically reduces the number of independent variables needed to completely describe all the possible behaviours of our model, reflecting a result called the |Buckingham pi theorem|.

Hydrostatic Waves
----------------------------
When :math:`\omega` is the diurnal frequency :math:`\frac{2\pi}{24\cdot 3600} \text{ s}^{-1} \approx 7.272 \times 10^{-5} \text{ s}^{-1}`, the term :math:`\frac{\omega^2}{N^2}` is tiny, and terms containing this factor can be neglected. Wave solutions for which :math:`\frac{\omega^2}{N^2} \approx 0` are called hydrostatic waves. The adjective "hydrostatic" reflects 

.. math::
    \frac{\omega^2}{N^2} \approx 0 \Rightarrow b \approx p_z,

i.e. that buoyancy forces are approximately balanced by vertical pressure gradient forces. In this context the balance is only approximate, and hence does not imply :math:`w=0`. Indeed, as we will see later, vertical velocities are essential to the core dynamics of gravity waves. The concept of "hydrostatic waves" is thus distinct from the usual "hydrostatic balance" condition :math:`\frac{\partial p}{\partial z} = -\rho g` we encounter in synoptic meteorology, which does imply :math:`w=0`.

In the land-sea breeze model above, :math:`\omega` is indeed the diurnal frequency, and so the model is mostly unresponsive to :math:`\frac{N}{\omega}`, except for the very smallest values of :math:`N`. Switching back to dimensional coordinates, we see that varying :math:`N` changes the tick labels on the :math:`x` axis in accordance with the scalings given above.

The Stream Function
---------------------------------------
Most of our models are solved analytically using a stream function. By way of introduction, consider the function :math:`\psi(x,z,t)` defined by

.. math::
    \psi(x,z,t) = \int_{z_0}^{z} u(x, z',t) \, dz' + f(x,t),

where :math:`z_0` is some arbitrary constant starting height and :math:`f(x)` is some function of :math:`x` alone. Provided :math:`u` is continuous for :math:`z'\in [z_0,z]`, the `first part of the fundamental theorem of calculus`_ implies :math:`\psi_z = u`. Now

.. math::
    \begin{align}
    \psi_x &= \frac{\partial}{\partial x} \left(\int_{z_0}^{z} u(x, z',t) \, dz' + f(x,t)\right) \\
    &= \int_{z_0}^{z} u_x(x, z',t) \, dz' + f_x(x,t),
    \end{align}

where the second line follows from the `Leibniz integral rule`_, noting neither :math:`z_0` or :math:`z` depend on :math:`x`. But the continuity equation for our Boussinesq fluid implies :math:`u_x = -w_z`, and so

.. math::
    \begin{align}
    \psi_x &=  \int_{z_0}^{z} -w_z(x, z',t) \, dz' + f_x(x,t) \\
    &= -w(x,z,t) + w(x,z_0,t) + f_x(x,t),
    \end{align}

where the second line follows from the `second part of the fundamental theorem of calculus`_, which holds provided :math:`w(x,z',t)` is continuous for :math:`z\in [z_0,z]`. Now, so far :math:`f(x,t)` has been arbitrary, but let's impose the additional condition that :math:`f_x(x,t):= -w(x,z_0,t)`. Then :math:`w=-\psi_x`. 

We have therefore found a scalar function :math:`\psi(x,z,t)`, which we call a stream function, which satisfies 

.. admonition:: Core Property of Stream Functions
    
    .. math::
        \begin{equation}
        (u,w) = (\psi_z, -\psi_x). 
        \end{equation}

Stream functions simplify things considerably. It's easier to solve for one scalar field :math:`\psi` than a vector field :math:`(u,w)`. Stream functions are also physically interpretable. In our case the :math:`(u,w)` winds are tangential to the contours of :math:`\psi` at all times, and the more closely packed the contours, the stronger the winds. Note that this does not imply parcel trajectories follow streamlines! You can study the relationship between :math:`\psi` and :math:`(u,w)` using the :ref:`applet <igw_intro_applet>` by switching the shading to :math:`\psi` and turning on the quiver plot.

Note stream functions are in general not unique; we can add any function :math:`g(t)` of :math:`t` alone to :math:`f(x,t)` and still have :math:`f_x(x,t):= -w(x,z_0,t)` and :math:`(u,w) = (\psi_z, -\psi_x)`.

The preceding argument shows stream functions exist provided :math:`u_x + w_z = 0`, and continuity conditions on :math:`u` and :math:`w` are satisfied. This is a special case of the `Poincaré lemma`_, typically taught in graduate `differential geometry`_ courses. [#]_

An Ordinary Differential Equation
------------------------------------------------------------------------
We now derive a single ordinary differential equation (ODE) for the stream function :math:`\psi`. We'll include some algebraic gore as it's our first time. To start, rewrite :math:`\text{\eqref{u_mom}-\eqref{b}}` by grouping the time tendency and diffusion terms; equations :math:`\eqref{u_mom}` and :math:`\eqref{v_mom}` become

.. math::
    \begin{align}
    \left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)u &= \frac{f}{\omega}v-p_x, \label{u_mom_grouped} \\
    \left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)v &= -\frac{f}{\omega}u. \label{v_mom_grouped}
    \end{align}

If expressions like :math:`\left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)` disturb you, you're not alone! Have a look at :ref:``   Take :math:`\left(\frac{\partial }{\partial t} + \frac{\alpha}{\omega}\right)` of :math:`\eqref{u_mom_grouped}` and substitute in :math:`\eqref{v_mom_grouped}` to get

.. math::
    \begin{equation}
    \left(\frac{\partial}{\partial t}+\frac{\alpha}{\omega}\right)^2 u = -\frac{f^2}{\omega^2}u - \left(\frac{\partial}{\partial t}+\frac{\alpha}{\omega}\right)p_x.
    \label{u_mom_alt}
    \end{equation}

Then take :math:`\frac{\partial}{\partial z}` of both sides of :math:`\eqref{u_mom_alt}` to get

.. math::
    \begin{equation}
    \left(\frac{\partial}{\partial t}+\frac{\alpha}{\omega}\right)^2 u_z = -\frac{f^2}{\omega^2}u_z - \left(\frac{\partial}{\partial t}+\frac{\alpha}{\omega}\right)p_{xz}.
    \label{u_mom_alt_z}
    \end{equation}

Next, rearrange :math:`\eqref{w_mom}` and take :math:`\left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)\frac{\partial}{\partial x}` of both sides to get

.. math::
    \begin{equation}
    \frac{\omega^2}{N^2}\left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)^2 w_x = \left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)b_x - \left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)p_{zx}.\label{w_mom_alt_x}
    \end{equation}

Now use :math:`\eqref{w_mom_alt_x}` to eliminate :math:`-\left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)p_{zx}` in :math:`\eqref{u_mom_alt_z}` to get

.. math::
    \begin{equation}
    \left(\frac{\partial}{\partial t}+\frac{\alpha}{\omega}\right)^2 u_z + \frac{f^2}{\omega^2}u_z = \frac{\omega^2}{N^2}\left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)^2 w_x - \left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)b_x.
    \label{u_w}
    \end{equation}

Next, rearrange :math:`\eqref{b}` and take an :math:`x` derivative of both sides to get

.. math::
    \begin{equation}
    -\left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)b_x = -Q_x + w_x \label{b_x}.
    \end{equation}

Now substitute :math:`\eqref{b_x}` into :math:`\eqref{u_w}` and rearrange to get

.. math::
    \begin{equation}
    \left(\frac{\partial}{\partial t}+\frac{\alpha}{\omega}\right)^2 u_z + \frac{f^2}{\omega^2}u_z - \frac{\omega^2}{N^2}\left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)^2 w_x - w_x = -Q_x.
    \label{u_w_alt}
    \end{equation}
    
Finally, substitute :math:`(u_z,w_x) = (\psi_{zz}, -\psi_{xx})` into :math:`\eqref{u_w_alt}` and group terms to get

.. admonition:: Governing Equation for :math:`\psi`
    
    .. math::
        \begin{equation}
        \left[\left(\frac{\partial}{\partial t}+\frac{\alpha}{\omega}\right)^2 + \frac{f^2}{\omega^2} \right] \psi_{xx} + \left[\frac{\omega^2}{N^2}\left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)^2 + 1\right] \psi_{xx}  = -Q_x.
        \label{psi_ode}
        \end{equation}

Models
-----------------

.. toctree::
    :maxdepth: 1

    land_sea.rst
    gaussian_forcing.rst
    localized_line_forcing.rst
    slope_breeze.rst
    point_forcing_over_slope.rst



Appendix A: Operators
-----------------------------------------------------------------------------

To get equation :math:`\eqref{u_mom_grouped}`, we implicitly used the fact that

.. math::
    \begin{equation}
    \frac{\partial u}{\partial t} + \frac{\alpha}{\omega}u = \left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)u. \label{grouped_terms}
    \end{equation}

Equations like :math:`\eqref{grouped_terms}` freaked me out when I first encountered them. For numbers :math:`a, b, c` we know multiplication distributes over addition, i.e. :math:`ac + bc = (a+b)c`, and equation :math:`\eqref{grouped_terms}` may therefore feel intuitive. However, :math:`\frac{\partial u}{\partial t}, u` and :math:`\frac{\partial}{\partial t}` are functions, not numbers! Even worse, :math:`\frac{\partial u}{\partial t}` and :math:`u` are functions mapping real vectors to real numbers, but :math:`\frac{\partial}{\partial t}` is a function mapping one function to another function, e.g. :math:`u \mapsto \frac{\partial u}{\partial t}`. So the distributive law for numbers isn't actually relevant here.

To make sense of equations like :math:`\eqref{grouped_terms}`, note that they express equalities of functions, not numbers; the same is true of most other equations on this page. Two functions are equal if their domains and co-domains are the same, and they map the same points in the domain to the same points in the co-domain. Furthermore, the additions and multiplications you see in equations like :math:`\eqref{grouped_terms}` actually express addition of functions, and multiplication of functions by numbers. For arbitrary functions :math:`f:A\to B` and :math:`g:A\to B`, we define :math:`f+g:A\to B` as the new function :math:`(f+g):A\to B` satisfying :math:`(f+g)(x) = f(x) + g(x)` for all :math:`x\in A`. In an analogous way, for a number :math:`a`, we define :math:`(af)(x) = af(x)`. You're probably used to doing all this without even thinking about it!

Things get confusing with expressions like :math:`\frac{\partial}{\partial t} + \frac{\alpha}{\omega}`. As noted above, :math:`\frac{\partial}{\partial t}` is really a function which acts on functions; such objects are typically called `operators`_. Analogously to above, we can define what it means to sum two operators, and multiply an operator by a function. Thus the expression :math:`\frac{\partial}{\partial t} + \frac{\alpha}{\omega}` is really a sum of two operators, where we must interpret :math:`\frac{\alpha}{\omega}` as the operator which sends a function, say :math:`u`, to the function :math:`\frac{\alpha}{\omega}u`. Using square brackets to enclose the function being fed into the given operator, we thus have

.. math::
    \left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)\left[u\right] = \frac{\partial}{\partial t}[u] + \frac{\alpha}{\omega}[u], 

by definition. In practice you will rarely see operators written out this way; typically we just assume operators "act from the left", i.e.

.. math:: 
    \left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)\left[u\right] = \frac{\partial}{\partial t}[u] + \frac{\alpha}{\omega}[u]

means the same thing as 

.. math::
    \left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)u = \frac{\partial u}{\partial t} + \frac{\alpha}{\omega}u.

However, suppressing the square brackets can be deceptive, as it may appear we are  "multiplying" terms like :math:`\left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)` and :math:`u`, rather than feeding :math:`u` into the operator :math:`\left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)`. Sometimes we really are multiplying though, in the sense of multiplying an operator by a function. For instance, you may see expressions like :math:`u\frac{\partial}{\partial t}`, which multiplies the function :math:`u` by the operator :math:`\frac{\partial}{\partial t}` to produce another operator; this operator is thus a completely different mathematical object to :math:`\frac{\partial}{\partial t}u`, which is a function! Similarly, you may see expressions like :math:`\left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)^2`, which should be interpreted as a composition of operators, i.e. :math:`\left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)\circ \left(\frac{\partial}{\partial t} + \frac{\alpha}{\omega}\right)`.

The ideas sketched in this appendix are made rigorous in `abstract algebra`_ and `functional analysis`_ courses. 

.. [#] In our applets we omit the :math:`*` subscripts, as the choice of dimensional or non-dimensional variables is clear from the radio button.

.. [#] In our applets we write the horizontal length scale simply as :math:`L` for both dimensional and non-dimensional coordinates, as javascript struggles with calligraphic math symbols, and the meaning of :math:`L` is clear from the context.

.. [#] `Batchelor's (1967, p. 76)`_ discussion of stream functions uses the language of exact and closed `differential forms`_, ideas from `differential geometry`_, and Batchelor appears to implicitly invoke the Poincaré lemma in his argument; I don't like this approach, as it invokes graduate level maths unnecessarily. You may have also encountered differential forms in thermodynamics, where they add an almost catastrophic level of confusion. See Bohrens & Albrecht (2023) for a scathing critique of differential forms in thermodynamics, with which I agree! 

.. _Boussinesq/shallow-anelastic: https://doi.org/10.1175/1520-0469(1962)019<0173:SAODAS>2.0.CO;2

.. _reduce the number of independent variables: https://en.wikipedia.org/wiki/Buckingham_%CF%80_theorem

.. |Buckingham pi theorem| raw:: html

   <a href="https://en.wikipedia.org/wiki/Buckingham_%CF%80_theorem">Buckingham \(\pi\) Theorem</a>

.. _Qian et al. (2009): https://doi.org/10.1175/2008JAS2851.1

.. _Rotunno (1983): https://doi.org/10.1175/1520-0469(1983)040<1999:OTLTOT>2.0.CO;2

.. _Batchelor (1967): https://doi.org/10.1017/CBO9780511800955

.. _Batchelor's (1967, p. 76): https://doi.org/10.1017/CBO9780511800955

.. _first part of the fundamental theorem of calculus: https://en.wikipedia.org/wiki/Fundamental_theorem_of_calculus#First_part

.. _second part of the fundamental theorem of calculus: https://en.wikipedia.org/wiki/Fundamental_theorem_of_calculus#Second_part

.. _Leibniz integral rule: https://en.wikipedia.org/wiki/Leibniz_integral_rule

.. _Poincaré lemma: https://en.wikipedia.org/wiki/Poincar%C3%A9_lemma

.. _differential forms: https://en.wikipedia.org/wiki/Differential_form

.. _differential geometry: https://en.wikipedia.org/wiki/Differential_geometry

.. _operators: https://en.wikipedia.org/wiki/Operator_(mathematics)

.. _abstract algebra: https://en.wikipedia.org/wiki/Abstract_algebra

.. _functional analysis: https://en.wikipedia.org/wiki/Functional_analysis

