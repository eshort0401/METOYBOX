The Anelastic Equations
===========================================================

Loosely speaking, the anelastic approximation is obtained by

    #. expressing the governing equations in buoyancy form.
    #. Replacing :math:`\rho` with a horizontally uniform :math:`\overline{\rho}(z)` wherever :math:`\rho` appears explicitly in the momentum and continuity equations.

Our governing momentum and continuity equations become

.. admonition:: Anelastic Equations
    
    .. math::
        \begin{align}
        \frac{D \mathbf{v}}{Dt} + f\mathbf{k}\times \mathbf{v} &= -\nabla \left(\frac{p}{\overline{\rho}}\right) + g\delta \phi \mathbf{k}, & \\
        \nabla \cdot \left(\overline{\rho} \mathbf{v}\right) &= 0 &
        \end{align}

The Boussinesq equations are very similar, but we instead replace :math:`\overline{\rho}` with a constant :math:`\rho_s` in the momentum and continuity equations (but nowhere else!)

.. _derivation:

Derivation of Anelastic System
------------------------------------------

I think `Ogura and Phillips (1962)`_ still provide the clearest derivation of the anelastic and Boussinesq equations, which we generalize slightly here. The core idea is to realize that for most of the motions we care about, fractional variations in potential temperature :math:`\epsilon = \frac{\theta - \theta_r}{\theta_r}` are small, where :math:`\theta_r` is some constant reference potential temperature. If we therefore expand our variables as power series in :math:`\epsilon` and keep just the first order terms, the residuals will be small.

To begin, we need to re-express our governing equations in a slightly different form. Consider the Exner-function :math:`\pi=\left(\frac{p}{p_r}\right)^\kappa`, where :math:`\kappa = \frac{R}{c_p}` and :math:`p_r` is a constant reference pressure, noting :math:`\theta=\frac{T}{\pi}`. Then

.. math::
    \begin{align*}
    -\frac{1}{\rho}\nabla p &= -\frac{1}{\rho}\frac{1}{\kappa}\pi^{\frac{1}{\kappa}-1}p_r \nabla \pi \\
    &= - T c_p \pi^{-1} \nabla \pi \\
    &= -c_p \theta \nabla \pi.
    \end{align*}

So our momentum equation can be written

.. math::
    \begin{align*}
    \frac{D\mathbf{v}}{Dt} &= -f\mathbf{k}\times\mathbf{v} -c_p \theta \nabla \pi - g \mathbf{k}.
    \end{align*}

The continuity equation can be re-expressed

.. math::
    \begin{align*}
    \frac{D}{Dt}\ln\left(\frac{\rho_r}{\rho}\right) = \nabla \cdot \mathbf{v}. \\
    \end{align*}

But note

.. math::
    \begin{align*}
    \ln\left(\frac{\rho_r}{\rho}\right) &= \ln\left( \rho_r \frac{RT}{p} \right)
    = \ln\left( \rho_r \frac{R\theta \pi}{p_r \pi^\frac{1}{\kappa} } \right) \\
    &= \ln\left( \theta \pi^{1-\frac{1}{\kappa}} \right) + \ln\left(\frac{R \rho_r}{p_r}\right). 
    \end{align*}

The term :math:`\ln\left(\frac{R \rho_r}{p_r}\right)` is constant, so our continuity equation becomes

.. math::
    \begin{align*}
    \frac{D}{Dt}\left[ \ln\theta + \left( 1-\frac{1}{\kappa} \right)\ln \pi \right] = \nabla \cdot \mathbf{v}. \\
    \end{align*}

.. _Vallis (2017, p. 75): https://doi.org/10.1017/9781107588417

.. _Taylor's theorem: https://en.wikipedia.org/wiki/Taylor%27s_theorem

.. _Big O notation: https://en.wikipedia.org/wiki/Big_O_notation

.. _Ogura and Phillips (1962): https://doi.org/10.1175/1520-0469(1962)019<0173:SAODAS>2.0.CO;2

.. _Exner function: https://en.wikipedia.org/wiki/Exner_function

.. _Batchelor (1967, p. 166): https://doi.org/10.1017/CBO9780511800955

.. _Durran (1989): https://doi.org/10.1175/1520-0469(1989)046<1453:ITAA>2.0.CO;2

.. _Klein (2010): https://doi.org/10.1146/annurev-fluid-121108-145537