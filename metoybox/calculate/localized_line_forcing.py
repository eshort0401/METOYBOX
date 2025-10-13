import numpy as np
from typing import List
from numpy.typing import NDArray
from metoybox.calculate.utils import recover_polarized_default


def calculate_constants(f_omega, alpha_omega, N_omega, sigma=1):
    """Calculate the constants used in the solution."""

    sigma_hat = 1j * sigma + alpha_omega
    B = np.sqrt(-(sigma_hat**2) - f_omega**2)
    C = np.sqrt(1 / N_omega**2 * sigma_hat**2 + 1)
    A = B / C
    if np.imag(1 / A) < 0:
        A = -A

    return A, B


def calculate_fields_spatial(
    X: NDArray,
    Z: NDArray,
    L: float,
    z_f: float,
    f_omega: float,
    alpha_omega: float,
    N_omega: float,
    fields: List[str] = ["psi", "u", "w"],
):
    """
    Calculate the spatial structures of the solutions. The full solutions are then,
    for instance, psi = np.real(psi_tilde * np.exp(1j * t)).
    """

    A, B = calculate_constants(f_omega, alpha_omega, N_omega)

    D = L * A * 1j / (4 * B**2)

    cond_1 = Z <= z_f
    cond_2 = Z > z_f

    L_1 = (1 / A * (z_f + Z) + X + 1j * L)[cond_1]
    L_2 = (1 / A * (z_f - Z) + X + 1j * L)[cond_1]
    L_3 = (1 / A * (-z_f + Z) + X - 1j * L)[cond_1]
    L_4 = (1 / A * (-z_f - Z) + X - 1j * L)[cond_1]

    L_5 = (1 / A * (z_f + Z) + X + 1j * L)[cond_2]
    L_6 = (1 / A * (-z_f + Z) + X + 1j * L)[cond_2]
    L_7 = (1 / A * (z_f - Z) + X - 1j * L)[cond_2]
    L_8 = (1 / A * (-z_f - Z) + X - 1j * L)[cond_2]

    psi = np.zeros_like(X, dtype=complex)
    u = np.zeros_like(X, dtype=complex)
    w = np.zeros_like(X, dtype=complex)
    phi = np.zeros_like(X, dtype=complex)

    psi[cond_1] = D * (-1 / L_1 + 1 / L_2 + 1 / L_3 - 1 / L_4)
    psi[cond_2] = D * (-1 / L_5 + 1 / L_6 + 1 / L_7 - 1 / L_8)

    u[cond_1] = D / A * (1 / L_1**2 + 1 / L_2**2 - 1 / L_3**2 - 1 / L_4**2)
    u[cond_2] = D / A * (1 / L_5**2 - 1 / L_6**2 + 1 / L_7**2 - 1 / L_8**2)

    w[cond_1] = -D * (1 / L_1**2 - 1 / L_2**2 - 1 / L_3**2 + 1 / L_4**2)
    w[cond_2] = -D * (1 / L_5**2 - 1 / L_6**2 - 1 / L_7**2 + 1 / L_8**2)

    fields_dict = {}
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
        sigma_hat = 1j + alpha_omega
        A_phi = -(sigma_hat + f_omega**2 / sigma_hat) * D / A
        phi[cond_1] = A_phi * (-1 / L_1 - 1 / L_2 + 1 / L_3 + 1 / L_4)
        phi[cond_2] = A_phi * (-1 / L_5 + 1 / L_6 - 1 / L_7 + 1 / L_8)
        fields_dict["phi"] = phi

    return fields_dict
