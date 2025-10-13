"""Code for calculating mountain-valley wave solutions."""

import numpy as np
from typing import List
from numpy.typing import NDArray

from metoybox.calculate.utils import recover_polarized_default


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
    sigma_hat = 1j + alpha_omega
    psi = M / B_sq * (exp_Z_sigma - 1)
    u = -M / B_sq * exp_Z_sigma
    w = -(M**2) / B_sq * exp_Z_sigma

    if "psi" in fields:
        fields_dict["psi"] = psi
    if "u" in fields:
        fields_dict["u"] = u
    if "w" in fields:
        fields_dict["w"] = w

    args = [u, w, f_omega, alpha_omega, fields]
    polarized_fields = recover_polarized_default(*args)
    fields_dict.update(polarized_fields)

    if "phi" in fields:
        if M == 0:
            fields_dict["phi"] = np.zeros_like(psi)
        else:
            fields_dict["phi"] = 1 / M * (-sigma_hat - f_omega**2) * u
    if "Q" in fields:
        fields_dict["Q"] = exp_Z_sigma.astype(np.complex128)
    if "bq" in fields:
        bq = 1 / sigma_hat * exp_Z_sigma
        fields_dict["bq"] = bq

    for key in fields_dict:
        # Mask values below the slope
        fields_dict[key][mask] = (1 + 1j) * np.nan

    return fields_dict
