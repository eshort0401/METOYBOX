The Anelastic Equations
===========================================================

.. admonition:: TODO:

    Either tighten up this page, or remove it entirely and just point readers to, for instance, `Klein (2010)`_. I like the javascript calculator below, but don't like the informality of the derivation.

Loosely speaking, the anelastic approximation is obtained by

    #. defining a base state, and using this to express the governing equations in buoyancy form.
    #. Replacing :math:`\rho` with a horizontally uniform :math:`\overline{\rho}(z)` wherever :math:`\rho` appears explicitly in the momentum and continuity equations.

Our governing momentum and continuity equations become

.. admonition:: Anelastic Equations
    
    .. math::
        \begin{align}
        \frac{D \mathbf{v}}{Dt} + f\mathbf{k}\times \mathbf{v} &= -\nabla \left(\frac{p}{\overline{\rho}}\right) + g\delta \phi \mathbf{k}, & \\
        \nabla \cdot \left(\overline{\rho} \mathbf{v}\right) &= 0 &
        \end{align}

The Boussinesq equations are very similar, but we instead replace :math:`\rho` with a constant :math:`\rho_s` in the momentum and continuity equations (but nowhere else!) 

.. _derivation:

Derivation of Anelastic System
------------------------------------------

Our approach here will be to expand key terms as Taylor series, but instead of immediately truncating, we will carry all the residual terms through to the bitter end, eventually performing a scale analysis to justify their final dismissal. To begin, we decompose our thermodynamic variables into hydrostatic and perturbation components. Let

.. math::
    \begin{align*}
    p &= \overline{p}(z) + \delta p(x,y,z,t), \\
    \rho &= \overline{\rho}(z) + \delta \rho(x,y,z,t), \\
    T &= \overline{T}(z) + \delta T(x,y,z,t),
    \end{align*}

where :math:`\overline{p}`, :math:`\overline{\rho}`, and :math:`\overline{T}` denote hydrostatic base state terms, assumed to be functions of :math:`z` only, with :math:`\delta p`, :math:`\delta \rho`, and :math:`\delta T` the corresponding perturbations. Now define :math:`\theta = \overline{\theta}(z) + \delta\theta,` where

.. math::
		\theta = T\left(\frac{p_s}{p}\right)^{\frac{R}{c_p}}, \quad \overline{\theta} = \overline{T}\left(\frac{p_s}{\overline{p}}\right)^{\frac{R}{c_p}},

with :math:`p_s` a constant reference pressure used to ensure dimensional consistency. Next, form

.. math::
	\begin{align}
	\overline{\phi} &= \ln\left(\frac{\overline{\theta}}{\theta_s}\right) = \frac{1}{\gamma}\ln\left(\frac{\overline{p}}{p_s}\right)  - \ln\left(\frac{\overline{\rho}}{\rho_s}\right), &\\
	\phi &= \ln\left(\frac{\theta}{\theta_s}\right) = \frac{1}{\gamma}\ln\left(\frac{\overline{p}+\delta p}{p_s}\right)  - \ln\left(\frac{\overline{\rho} + \delta \rho}{\rho_s}\right), &
	\end{align}

with :math:`\gamma = \frac{c_v}{c_p}` and :math:`\theta_s` and :math:`\rho_s` constant reference values. Now, assume :math:`\delta p < \overline{p}`, and :math:`\delta \rho < \overline{\rho}`. Then

.. math::
	\begin{align}
	\delta \phi = \phi - \overline{\phi} &=  \frac{1}{\gamma}\ln\left(\frac{\overline{p} + \delta p}{\overline{p}}\right)  - \ln\left(\frac{\overline{\rho}+\delta \rho}{\overline{\rho}}\right) & \label{eq:delphi_og} \\
	&=  \frac{1}{\gamma}\frac{\delta p}{\overline{p}} + R_1 - \frac{\delta \rho}{\overline{\rho}}  + R_2 \label{eq:delphi} &
	\end{align}

by `Taylor's theorem`_, where

.. math::
    \begin{align*}
    R_1 &= \frac{1}{\gamma}\left[-\frac{1}{2}\left(\frac{\delta p}{\overline{p}}\right)^2 + \frac{1}{3}\left(\frac{\delta p}{\overline{p}}\right)^3 + \cdots \right] = O\left[\left(\frac{\delta p}{\overline{p}}\right)^2\right]\\ 
    R_2 &= -\frac{1}{2}\left(\frac{\delta \rho}{\overline{\rho}}\right)^2 + \frac{1}{3}\left(\frac{\delta \rho}{\overline{\rho}}\right)^3 + \cdots = O\left[\left(\frac{\delta \rho}{\overline{\rho}}\right)^2\right].
    \end{align*}

The `Big O notation`_ means the magnitudes of :math:`R_1` and :math:`R_2` are bounded by functions proportional to :math:`\left(\frac{\delta p}{\overline{p}}\right)^2` and :math:`\left(\frac{\delta \rho}{\overline{\rho}}\right)^2`, respectively. Note, these sums require :math:`\frac{\delta p}{\overline{p}} < 1` and :math:`\frac{\delta \rho}{\overline{\rho}} < 1` to converge, hence our assumptions above. Note also that

.. math::
    g\delta \phi = g\ln\left(\frac{\overline{\theta} + \delta \theta}{\overline{\theta}}\right) = g\frac{\delta \theta}{\overline{\theta}} + O\left(\left[\frac{\delta \theta}{\overline{\theta}}\right]^2\right)

is buoyancy :math:`b` in the anelastic system. Furthermore,

.. math::
	\begin{align}
	\frac{\partial \overline{\phi}}{\partial z} &= \frac{1}{\gamma \overline{p}}\frac{\partial \overline{p}}{\partial z} - \frac{1}{ \overline{\rho}}\frac{\partial \overline{\rho}}{\partial z} &\nonumber \\
	&= -\frac{g \overline{\rho}}{\gamma \overline{p}} - \frac{1}{ \overline{\rho}}\frac{\partial \overline{\rho}}{\partial z} \label{eq:bar_phi_z} &
	\end{align}

as the base state is hydrostatic.

Now, the inviscid horizontal momentum equation is

.. math::
    \begin{align}
	\frac{D\mathbf{u}}{Dt} + f\mathbf{k}\times \mathbf{u} &= -\frac{1}{\overline{\rho}+\delta \rho}\nabla_h \delta p, & \nonumber \\
    &= -\frac{1}{\overline{\rho}} \nabla_h \delta p + R_3 \nabla_h \delta p, & \label{eq:anumom}
    \end{align}

where :math:`\nabla_h = \left(\frac{\partial }{\partial x}, \frac{\partial }{\partial y} \right)` is the horizontal gradient operator, :math:`\mathbf{u}=(u,v)` is the horizontal velocity, and

.. math::
    \begin{equation}
    R_3 = O\left(\frac{\delta \rho}{\overline{\rho}^2}\right),
    \end{equation}

exploiting Taylor's theorem once again.

The vertical momentum equation implies

.. math::
    \begin{align}
	(\overline{\rho} + \delta \rho)\frac{D w}{Dt} &= -\frac{\partial \left(\overline{p} + \delta p \right)}{\partial z} - g\left( \overline{\rho} + \delta\rho \right) & \nonumber \\ 
    &= -\frac{\partial \delta p}{\partial z} - g\delta \rho, &
    \end{align}

where the second line follows from the hydrostasy of the base state. Dividing through by :math:`\overline{\rho} + \delta \rho` gives

.. math::
    \begin{align}
	\frac{D w}{Dt} &= -\frac{1}{\overline{\rho}}\frac{\partial \delta p}{\partial z} - g\frac{\delta \rho}{\overline{\rho}} + R_3\left(-\frac{\partial \delta p}{\partial z} - g\delta\rho \right) \\
    &=-\frac{\partial}{\partial z}\left(\frac{\delta p}{\overline{\rho}}\right) - \frac{\delta p}{\overline{\rho}^2}\frac{\partial \overline{\rho}}{\partial z} - g\frac{\delta \rho}{\overline{\rho}} + R_3\left(-\frac{\partial \delta p}{\partial z} - g\delta\rho \right).
    \end{align}

Substituting for :math:`-g\frac{\delta \rho}{\overline{\rho}}` using :math:`g\times \eqref{eq:delphi}` results in

.. math::
	\frac{D w}{Dt} = -\frac{\partial}{\partial z}\left(\frac{\delta p}{\overline{\rho}}\right) - \frac{\delta p}{\overline{\rho}^2}\frac{\partial \overline{\rho}}{\partial z} + g\delta \phi - \frac{g}{\gamma}\frac{\delta p}{\overline{p}} + R_4,


where we define

.. math::
    R_4 = -gR_1 - gR_2 + R_3\left(-\frac{\partial \delta p}{\partial z} - g\delta\rho \right)

for convenience.

Substituting the second and fourth terms using :math:`\frac{\delta p}{\overline{\rho}}\times\eqref{eq:bar_phi_z}` gives

.. math::
    \begin{equation}
	\frac{D w}{Dt} =  g\delta \phi -\frac{\partial}{\partial z}\left(\frac{\delta p}{\overline{\rho}}\right) +\frac{\delta p}{\overline{\rho}}\frac{\partial \overline{\phi}}{\partial z} + R_4. \label{eq:w_t_intermediate}
    \end{equation}


Now suppose we also require that the base state is neutrally stratified, i.e. that :math:`\overline{\theta}`, and therefore :math:`\overline{\phi}`, are constant. Then :math:`\eqref{eq:w_t_intermediate}` reduces to

.. math::
    \begin{equation}
	\frac{D w}{Dt} =  g\delta \phi -\frac{\partial}{\partial z}\left(\frac{\delta p}{\overline{\rho}}\right) + R_4. \label{eq:anwmom}
    \end{equation}


Finally, recall mass conservation is given by

.. math::
    \begin{equation}
	\frac{\partial \delta \rho}{\partial t} + \nabla \cdot \left[\left(\overline{\rho} + \delta \rho\right)\mathbf{v}\right] = 0.
    \end{equation}

which we re-express as 

.. math::
    \begin{equation}
	\frac{\partial \delta \rho}{\partial t} + \nabla_h \cdot \left(\overline{\rho} \mathbf{u}\right) + \frac{\partial}{\partial z}\left(\overline{\rho} w\right) + \nabla \cdot \left(\delta \rho \mathbf{v}\right) = 0. \label{eq:anmass}
    \end{equation}

Now, we want to perform a scale-analysis, i.e. explore circumstances where the residual terms in :math:`\eqref{eq:anumom}`, :math:`\eqref{eq:anwmom}`, and the :math:`\delta \rho` terms in :math:`\eqref{eq:anmass}`, are much smaller than the other terms. The most rigorous approach involves distinguished limits and asymptotic expansions [#]_, but let's instead aim for accessibility. First, write all our variables as a number times a function with an order of magnitude of around 1; 

.. math::
    \begin{align*}
    \mathbf{u} = U\widehat{\mathbf{u}}, \quad w = W\widehat{w}, \quad (x, y) = L\left(\widehat{x}, \widehat{y}\right), \quad z = H\widehat{z}, \quad t = T\widehat{t}, \\
    \overline{\rho} = \overline{R} \widehat{\overline{\rho}}, \quad \delta \rho = \Delta R \widehat{\delta \rho}, \quad \overline{p} = \overline{P} \widehat{\overline{p}}, \quad \delta p = \Delta P \widehat{\delta p}, \quad \delta \phi = \Delta \Phi \widehat{\delta \phi}.
    \end{align*}

Just as there are relationships between our variables, there will be relationships between the numbers :math:`U,W,L` etc. Let's specify the scales :math:`L`, :math:`U`, :math:`W`, :math:`\Delta P` and :math:`\Delta R`, and infer the others. Because we assumed :math:`\delta \rho < \overline{\rho}`, :math:`\eqref{eq:anumom}` implies

.. math::
    \begin{equation*}
    \Delta P \sim \max\left(\overline{R} U^2, \overline{R} f UL\right),
    \end{equation*}

using :math:`\sim` to mean "about the same order of magnitude". Note :math:`\Delta P \sim \overline{R}fUL` represents geostrophic balance. Next, :math:`\eqref{eq:anwmom}` implies

.. math::
    \begin{equation*}
    \Delta R = \max\left(\frac{W^2}{H}\frac{\overline{R}}{g}, \frac{1}{g}\frac{\Delta P}{H} \right),
    \end{equation*}

noting :math:`\Delta R \sim \frac{\Delta P}{gH}` represents hydrostatic balance. The scale for :math:`\Delta \Phi` follows from :math:`\eqref{eq:delphi_og}`. Now let's put all this in a javascript table so you can play around with the scales and check the sizes of the residuals. Note I blank out cases where we end up with :math:`\Delta P > \overline{P}` or :math:`\Delta R > \overline{R}`, as such situations violate our earlier assumptions.

.. raw:: html
    :file: ../_static/calculators/anelastic/anelastic.html

Derivation of Boussinesq System
------------------------------------------------------------------------

.. admonition:: TODO:

    Comment on adapting the above to the Boussinesq case.

Extensions
------------------------------------------------------------------------
Both the anelastic and Boussinesq systems can be made more numerically accurate by using the Exner function; see `Ogura and Phillips (1962)`_. `Durran (1989)`_ has also grappled with the anelastic system, seeking to remove the requirement of a neutrally stratified base state. See `Klein (2010)`_ for a more rigorous review.


.. [#] See for instance `Ogura and Phillips (1962)`_ and `Klein (2010)`_.

.. _Vallis (2017, p. 75): https://doi.org/10.1017/9781107588417

.. _Taylor's theorem: https://en.wikipedia.org/wiki/Taylor%27s_theorem

.. _Big O notation: https://en.wikipedia.org/wiki/Big_O_notation

.. _Ogura and Phillips (1962): https://doi.org/10.1175/1520-0469(1962)019<0173:SAODAS>2.0.CO;2

.. _Exner function: https://en.wikipedia.org/wiki/Exner_function

.. _Batchelor (1967, p. 166): https://doi.org/10.1017/CBO9780511800955

.. _Durran (1989): https://doi.org/10.1175/1520-0469(1989)046<1453:ITAA>2.0.CO;2

.. _Klein (2010): https://doi.org/10.1146/annurev-fluid-121108-145537