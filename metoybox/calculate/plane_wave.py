import numpy as np
from scipy.special import expi as sp_expi
from typing import List
from numpy.typing import NDArray
from metoybox.calculate.utils import recover_polarized_default


def calculate_constants(f_omega, alpha_omega, N_omega, sigma):
    """Calculate the constants used in the solution."""

    sigma_hat = 1j * sigma + alpha_omega
    B = np.sqrt(-(sigma_hat**2) - f_omega**2)
    C = np.sqrt(1 / N_omega**2 * sigma_hat**2 + 1)
    B, C = np.complex128(B), np.complex128(C)
    A = B / C
    if np.imag(1 / A) < 0:
        A = -A
    return A, B


def calculate_fields_spatial(
    X: NDArray,
    Z: NDArray,
    k: float,
    sigma: float,
    f_omega: float,
    alpha_omega: float,
    N_omega: float,
    fields: List[str] = ["psi", "u", "w"],
):
    """
    Calculate the spatial structures of the solutions. The full solutions are then,
    for instance, psi = np.real(psi_tilde * np.exp(1j * t)).
    """
    A, B = calculate_constants(f_omega, alpha_omega, N_omega, sigma)

    m = k / A
    # Use an amplitude of 0.1 for psi to get plausible dimensional values
    psi = 0.1*np.exp(1j * (k * X + m * Z))
    u = 1j * m * psi
    w = -1j * k * psi

    fields_dict = {}
    fields_dict["psi"] = psi
    fields_dict["u"] = u
    fields_dict["w"] = w

    args = [u, w, f_omega, alpha_omega, fields, sigma]
    polarized_fields = recover_polarized_default(*args)
    fields_dict.update(polarized_fields)

    sigma_hat = 1j * sigma + alpha_omega

    phi = -(sigma_hat + f_omega**2 / sigma_hat) * m / k * psi
    fields_dict["phi"] = phi

    return fields_dict
