"""Code for calculating mountain-valley wave solutions."""

import numpy as np
from typing import Dict, List, Union
from numpy.typing import NDArray


def calculate_tilde(
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
    B_sq = (
        -((1j + alpha_omega) ** 2) * (1 + (1 / N_omega**2) * M**2) - f_omega**2 - M**2
    )
    exp_Z_sigma = np.exp(-Z_sigma)

    psi_tilde = M / B_sq * (exp_Z_sigma - 1)
    u_tilde = -M / B_sq * exp_Z_sigma
    w_tilde = -(M**2) / B_sq * exp_Z_sigma
    Q_tilde = exp_Z_sigma

    mask = Z < M * X
    psi_tilde[mask] = np.nan
    u_tilde[mask] = np.nan
    w_tilde[mask] = np.nan
    Q_tilde[mask] = np.nan

    fields_dict = {"psi": psi_tilde, "u": u_tilde, "w": w_tilde, "Q": Q_tilde}
    return fields_dict
