"""Code for calculating mountain-valley wave solutions."""

import numpy as np
from typing import List
from numpy.typing import NDArray


def calculate_fields_spatial(
    X: NDArray,
    Z: NDArray,
    M: float,
    f_omega: float,
    alpha_omega: float,
    N_omega: float,
    fields: List[str] = ["psi", "u", "w", "Q"],
):
    """
    Calculate the spatial structures of the solutions. The full solutions are then,
    for instance, psi = np.real(psi_tilde * np.exp(1j * t)).
    """

    Z_sigma = Z - M * X
    B_sq = -((1j + alpha_omega) ** 2) * (1 + (1 / N_omega**2) * M**2)
    B_sq += -(f_omega**2) - M**2
    exp_Z_sigma = np.exp(-Z_sigma)

    mask = Z < M * X

    fields_dict = {}
    base = 1 / B_sq * exp_Z_sigma
    sigma_hat = 1j + alpha_omega

    if "psi" in fields:
        psi = M / B_sq * (exp_Z_sigma - 1)
        psi[mask] = (1 + 1j) * np.nan
        fields_dict["psi"] = psi
    if "u" in fields:
        u = -M * base
        u[mask] = (1 + 1j) * np.nan
        fields_dict["u"] = u
    if "w" in fields:
        w = -(M**2) * base
        w[mask] = (1 + 1j) * np.nan
        fields_dict["w"] = w
    if "v" in fields:
        v = f_omega * M / (1j + alpha_omega) * base
        v[mask] = (1 + 1j) * np.nan
        fields_dict["v"] = v
    if "xi" in fields:
        xi = 1j * M * base
        xi[mask] = (1 + 1j) * np.nan
        fields_dict["xi"] = xi
    if "zeta" in fields:
        zeta = 1j * (M**2) * base
        zeta[mask] = (1 + 1j) * np.nan
        fields_dict["zeta"] = zeta
    if "phi" in fields:
        phi = sigma_hat * base + f_omega**2 / sigma_hat * base
        phi[mask] = (1 + 1j) * np.nan
        fields_dict["phi"] = phi
    if "Q" in fields:
        Q = exp_Z_sigma.astype(np.complex128)
        Q[mask] = (1 + 1j) * np.nan
        fields_dict["Q"] = Q

    return fields_dict
