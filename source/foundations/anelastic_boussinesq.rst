The Anelastic Equations
==============================================

To get the anelastic equations we do the following.

    #. Define a base state, and use this to express our equations in buoyancy form.
    #. Replace :math:`\rho` with a horizontally uniform :math:`\overline{\rho}(z)` wherever :math:`\rho` appears explicitly in the momentum and continuity equations.

The Boussinesq equations are a sub-case of the anelastic, with :math:`\overline{\rho}(z)` taken to be a constant :math:`\rho_s`. 

The anelastic approximation filters sound-waves from our system of equations. Back in the day, this filtering had computational advantages when integrating numerically, but we don't care about that here. We like the anelastic approximation because it allows us to play with the maths more directly. 

Building intuition for the scope of validity and physical implications of the anelastic approximation has been tortuously difficult for me. One challenge is that different authors use the terms "incompressible", "anelastic" and "Boussinesq" for different things. Another challenge is that the governing equations can be written in buoyancy form using many distinct coordinate systems, resulting in many different equation sets and lots of very technical papers, with :math:`*` and :math:`\overline{\,}` symbols spilling out everywhere.

Below I give a loose derivation mostly plagiarized from `Vallis (2017, p. 75)`_. This derivation uses our standard variables :math:`x,y,z,\rho,p` and so forth, making the maths easier to interpret. However, using garden variety variables results in approximations less numerically accurate than those associated with more exotic variables, to be discussed later. 

.. _derivation:

Derivation
---------------------------

Let

.. math::
    \begin{align*}
    p &= \overline{p}(z) + \delta p(x,y,z,t), \\
    \rho &= \overline{\rho}(z) + \delta \rho(x,y,z,t), \\
    T &= \overline{T}(z) + \delta T(x,y,z,t),
    \end{align*}

where :math:`\overline{p}`, :math:`\overline{\rho}`, and :math:`\overline{T}` denote hydrostatic base state variables, assumed to be functions of :math:`z` only, with :math:`\delta p`, :math:`\delta \rho`, and :math:`\delta T` the corresponding perturbations. Now define :math:`\theta = \overline{\theta}(z) + \delta\theta`, where

.. math::
		\theta = T\left(\frac{p_s}{p}\right)^{\frac{R}{c_p}}, \quad \overline{\theta} = \overline{T}\left(\frac{p_s}{\overline{p}}\right)^{\frac{R}{c_p}},

with :math:`p_s = \overline{p}(0)`.

Next, define

.. math::
	\begin{align}
	\overline{\phi} &= \ln\left(\frac{\overline{\theta}}{\theta_s}\right) = \frac{1}{\gamma}\ln\left(\frac{\overline{p}}{p_s}\right)  - \ln\left(\frac{\overline{\rho}}{\rho_s}\right), &\\
	\phi &= \ln\left(\frac{\theta}{\theta_s}\right) = \frac{1}{\gamma}\ln\left(\frac{\overline{p}+\delta p}{p_s}\right)  - \ln\left(\frac{\overline{\rho} + \delta \rho}{\rho_s}\right), &
	\end{align}

with :math:`\theta_s = \overline{\theta}(0)` and :math:`\rho_s = \overline{\rho}(0)`. Note the subscript :math:`s` terms are there because I'm pedantic about unit consistency; we are not restricting to the Boussinesq system yet! Continuing,

.. math::
	\begin{align}
	\delta \phi = \phi - \overline{\phi} &=  \frac{1}{\gamma}\ln\left(\frac{\overline{p} + \delta p}{\overline{p}}\right)  - \ln\left(\frac{\overline{\rho}+\delta \rho}{\overline{\rho}}\right) & \nonumber \\
	&=  \frac{1}{\gamma}\frac{\delta p}{\overline{p}}  - \frac{\delta \rho}{\overline{\rho}} + O\left(\left[\frac{\delta p}{\overline{p}}\right]^2\right) + O\left(\left[\frac{\delta \rho}{\overline{\rho}}\right]^2\right) \label{eq:delphi_raw} &
	\end{align}

by Taylor's Theorem, where :math:`\gamma = \frac{c_v}{c_p}`. Note :math:`g\delta \phi = g\ln\left(\frac{\overline{\theta} + \delta \theta}{\overline{\theta}}\right) = g\frac{\delta \theta}{\overline{\theta}} + O\left(\left[\frac{\delta \theta}{\overline{\theta}}\right]^2\right)` corresponds to buoyancy :math:`b` provided :math:`\left[\frac{\delta \theta}{\overline{\theta}}\right]^2` is small. Similarly, if :math:`\left[\frac{\delta p}{\overline{p}}\right]^2` and :math:`\left[\frac{\delta \rho}{\overline{\rho}}\right]^2` are small, we may discard the associated terms in :math:`\eqref{eq:delphi_raw}` to get

.. math::
	\begin{equation}
	\delta \phi  = \frac{1}{\gamma}\frac{\delta p}{\overline{p}}  - \frac{\delta \rho}{\overline{\rho}}.
    \label{eq:delphi}
    \end{equation}

Also,

.. math::
	\begin{align}
	\frac{\partial \overline{\phi}}{\partial z} &= \frac{1}{\gamma \overline{p}}\frac{\partial \overline{p}}{\partial z} - \frac{1}{ \overline{\rho}}\frac{\partial \overline{\rho}}{\partial z} \nonumber \\
	&= -\frac{g \overline{\rho}}{\gamma \overline{p}} - \frac{1}{ \overline{\rho}}\frac{\partial \overline{\rho}}{\partial z} \label{eq:bar_phi_z}
	\end{align}

as the base state is hydrostatic.

Having setup all our base state and perturbation variables, we can now re-express our governing equations. Ignoring viscosity, the horizontal momentum equation is

.. math::
	(\overline{\rho}+\delta \rho)\left[\frac{D\mathbf{u}}{Dt} + f\mathbf{k}\times \mathbf{u} \right] = -\nabla_h \delta p,

where :math:`\nabla_h = \left(\frac{\partial }{\partial x}, \frac{\partial }{\partial y} \right)` is the horizontal gradient operator, and :math:`\mathbf{u}=(u,v)` is the horizontal velocity. Neglecting :math:`\delta \rho` on the left hand side, we obtain

.. math::
	\frac{D\mathbf{u}}{Dt} + f\mathbf{k}\times \mathbf{u} = - \nabla_h \frac{\delta p}{\overline{\rho}}.


The vertical momentum equation is

.. math::
    \begin{align}
	(\overline{\rho} + \delta \rho)\frac{D w}{Dt} &= -\frac{\partial \left(\overline{p} + \delta p \right)}{\partial z} - g\left( \overline{\rho} + \rho \right) \nonumber \\ 
    &= -\frac{\partial \delta p}{\partial z} - g\delta \rho,
    \end{align}

exploiting the hydrostasy of the base state. Neglecting :math:`\delta \rho` on the left hand side and rearranging gives

.. math::
	\frac{D w}{Dt} = -\frac{\partial}{\partial z}\left(\frac{\delta p}{\overline{\rho}}\right) - \frac{\delta p}{\overline{\rho}^2}\frac{\partial \overline{\rho}}{\partial z} - g\frac{\delta \rho}{\overline{\rho}}.

Substituting for :math:`g\frac{\delta \rho}{\overline{\rho}}` using equation :math:`\eqref{eq:delphi}` gives

.. math::
	\frac{D w}{Dt} = -\frac{\partial}{\partial z}\left(\frac{\delta p}{\overline{\rho}}\right) - \frac{\delta p}{\overline{\rho}^2}\frac{\partial \overline{\rho}}{\partial z} + g\delta \phi - \frac{g}{\gamma}\frac{\delta p}{\overline{p}}.

Substituting the second and fourth terms using :math:`\frac{\delta p}{\overline{\rho}}\times\eqref{eq:bar_phi_z}` gives

.. math::
    \begin{equation}
	\frac{D w}{Dt} =  g\delta \phi -\frac{\partial}{\partial z}\left(\frac{\delta p}{\overline{\rho}}\right) +\frac{\delta p}{\overline{\rho}}\frac{\partial \overline{\phi}}{\partial z}. \label{eq:w_t_intermediate}
    \end{equation}

Now consider the expressions

.. math::
	\left|\frac{\partial}{\partial z} \ln\left(\frac{\delta p / p_s}{\overline{\rho} / \rho_s}\right)\right|, \quad \left|\frac{\partial}{\partial z} \ln\left(\frac{\overline{\theta}}{\theta_s}\right)\right|.

In most of the atmospheres we care about, the pressure and density scale heights are of similar magnitude, but the  potential temperature scale height is much larger, so the first term above is typically much larger than the second. This implies the second term in :math:`\eqref{eq:w_t_intermediate}` is much larger in absolute value than the third, which we discard. We thus have

.. math::
    \begin{equation}
	\frac{D w}{Dt} =  g\delta \phi -\frac{\partial}{\partial z}\left(\frac{\delta p}{\overline{\rho}}\right).\label{eq:w}
    \end{equation}


We can therefore write the anelastic momentum equations in vector form as

.. math::
	\begin{equation}
	\frac{D \mathbf{v}}{Dt} + f\mathbf{k}\times \mathbf{v} = -\nabla \left(\frac{p}{\overline{\rho}}\right) + g\delta \phi \mathbf{k},
    \label{eq:anmom}
    \end{equation}

where :math:`\mathbf{v}=(u, v, w)`.

Mass conservation is given by

.. math::
	\frac{\partial \delta \rho}{\partial t} + \nabla \cdot \left[\left(\overline{\rho} + \delta \rho\right)\mathbf{v}\right] = 0,

which after discarding :math:`\delta \rho` terms becomes

.. math::
	\nabla \cdot \left(\overline{\rho} \mathbf{v}\right) = 0.


Summarizing, we have

.. admonition:: Anelastic Equations
    
    .. math::
        \begin{align}
        \frac{D \mathbf{v}}{Dt} + f\mathbf{k}\times \mathbf{v} &= -\nabla \left(\frac{p}{\overline{\rho}}\right) + g\delta \phi \mathbf{k}, & \\
        \nabla \cdot \left(\overline{\rho} \mathbf{v}\right) &= 0 &
        \end{align}


Exploration
-------------------------------------------------------------------
Let's explicitly compare the magnitudes of terms in all the equations of our :ref:`derivation <derivation>` where things were discarded.

.. raw:: html
    :file: ../_static/calculators/anelastic_vallis/anelastic_vallis.html

.. _Vallis (2017, p. 75): https://doi.org/10.1017/9781107588417