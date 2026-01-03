Anelastic Vorticity Equation
=================================

Recall the anelastic momentum equation is 

.. math::
	\begin{equation}
	\frac{D \mathbf{v}}{Dt} + f\mathbf{k}\times \mathbf{v} = -\nabla \left(\frac{p}{\rho_0}\right) + g\delta \phi \mathbf{k},
    \label{eq:anmom}
    \end{equation}

where :math:`\mathbf{v}=(u, v, w)`.

Let :math:`\nabla \mathbf{v}` denote the matrix (i.e. tensor) with columns one, two, and three containing the gradient of :math:`u, v, w`, respectively. Note

.. math::
	\begin{align}
	\mathbf{v} \cdot \nabla\mathbf{v} &= \left(u,v,w\right)
	\begin{pmatrix}
	u_x & v_x & w_x \\
	u_y & v_y & w_y \\
	u_z & v_z & w_z \\
	\end{pmatrix}\\
	&= \left(uu_x+vu_y+wu_z, uv_x+vv_y+wv_z, uw_x+vw_y+ww_z\right) \\
	&= \nabla\frac{|\mathbf{v}|^2}{2}+\left(vu_y+wu_z-vv_x-ww_x, uv_x+wv_z-uu_y-ww_y, uw_x+vw_y-uu_z-vv_z\right)\\
	&=\nabla\frac{|\mathbf{v}|^2}{2}+ 
	\begin{vmatrix}
	\mathbf{i} & \mathbf{j} & \mathbf{k} \\
	w_y-v_z & u_z-w_x & v_x - u_y \\
	u & v & w 
	\end{vmatrix} \\
	&=\nabla\frac{|\mathbf{v}|^2}{2}+ \boldsymbol{\omega}\times\mathbf{v}
	\end{align}


Following Markowski (2010, p. 21), to derive the vorticity equation, take the curl of both sides of equation :math:`\eqref{eq:anmom}` and apply vector identities to obtain

.. math::
	\begin{align}
	\nabla\times\left(\frac{D \mathbf{v}}{Dt} + f\mathbf{k}\times \mathbf{v}\right) &= -\nabla \left(\frac{p}{\rho_0}\right) + g\delta \phi \mathbf{k} \\
	\frac{D(\boldsymbol{\omega} + f \mathbf{k})}{Dt} + (\boldsymbol{\omega} + f \mathbf{k})(\nabla\cdot \mathbf{v}) &= \left[\left(\boldsymbol{\omega} + f \mathbf{k}\right)\cdot \nabla\right]\mathbf{v} + \nabla \times \left(g\delta \phi \mathbf{k}\right),
	\end{align}

where :math:`\boldsymbol{\omega} = (\xi, \eta, \zeta)` is the vorticity vector, and :math:`\nabla \mathbf{v}` is a tensor. Considering just the :math:`y` component,

.. math::
	\frac{D\eta}{Dt} + \eta\left[u_x + v_y + w_z\right] = 
	\left(\boldsymbol{\omega}+f\mathbf{k}\right)\cdot\nabla v + g\phi_x,

where :math:`x, y, z` subscripts denote partial derivatives. The continuity equation implies

.. math::
	-w \eta \frac{1}{\rho_0}\frac{\partial \rho_0}{\partial z} = \eta\left[u_x + v_y + w_z\right].

Substituting into the previous equation and multiplying through by :math:`\frac{1}{\rho_0}` gives

.. math::
	\begin{equation}
	\frac{D}{Dt}\left(\frac{\eta}{\rho_0}\right) = \underbrace{\frac{1}{\rho_0}\left(\boldsymbol{\omega}+f\mathbf{k}\right)\cdot\nabla v}_{\text{deformation}} + \underbrace{\frac{g}{\rho_0}\frac{\partial \phi}{\partial x}}_{\text{generation}}.
    \label{eq:vort}
    \end{equation}

The quantity :math:`\frac{\boldsymbol{\omega}}{\rho_0}` is sometimes called "specific-vorticity" (Petropoulos et al., 2017). Equation :math:`\eqref{eq:vort}` says that the horizontal component of a parcel's (anelastic) specific vorticity can change only through vorticity deformation or baroclinic vorticity generation. In the absence of deformation and generation, if a parcel's specific volume increases, its horizontal vorticity :math:`\eta` must decrease, behavior analogous to that of angular momentum.