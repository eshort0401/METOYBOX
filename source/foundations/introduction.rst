Introduction
=======================================================

.. admonition:: TODO:

    Some general comments on maths, logic etc, and the peculiarities of atmospheric science, could be valuable here. Could be adapted from chapters 1 and 2 of my `thesis <https://hdl.handle.net/11343/350333>`_.

.. admonition:: Governing Equations for a Dry Atmosphere   
    
    .. math::
        \begin{align}
        \frac{D \mathbf{v}}{Dt}&=-f\mathbf{k}\times\mathbf{v}-\frac{1}{\rho}\nabla p+\mathbf{g}+\mathbf{F}, & \label{Eq:mom_simp} \\
        \frac{D\rho}{Dt}&=-\rho(\nabla\cdot \mathbf{v}), & \label{Eq:con_mass} \\
        \frac{Ds}{Dt} &= \frac{D}{Dt}\left[c_p\ln\left(\frac{\theta}{T_0}\right)\right] =\frac{q}{T}, & \label{Eq:cons_energy} \\
        p &= \rho R T, & \label{Eq:state}
        \end{align}

