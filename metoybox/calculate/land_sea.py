import numpy as np
from scipy.special import expi as sp_expi
from typing import List
from numpy.typing import NDArray
from metoybox.calculate.utils import recover_polarized_default


def expi(z, theta_b=np.pi / 2):
    """
    Calculates the exponential integral Ei(z) with a custom branch cut in direction
    theta_b.
    """
    principal_value = sp_expi(z)
    z_angle = np.angle(z)
    correction = np.zeros_like(principal_value, dtype=np.complex128)
    if 0 <= theta_b < np.pi:
        mask = (z_angle > theta_b) & (z_angle <= np.pi)
        correction[mask] = -2j * np.pi
    elif -np.pi < theta_b < 0:
        mask = (z_angle > -np.pi) & (z_angle < theta_b)
        correction[mask] = 2j * np.pi
    return principal_value + correction


def calculate_constants(f_omega, alpha_omega, N_omega, sigma=1):
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
    L: float,
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

    X_piL = X + 1j * L
    X_miL = X - 1j * L

    L_1 = (1 / A) * Z + X_piL
    L_2 = -(1 / A) * Z + X_miL

    I = np.zeros_like(Z, dtype=complex)

    D = -1 / (B**2 * 4 * np.pi * 1j)

    I_1 = -np.exp(A * L_1) * (-1j * np.pi - expi(-A * L_1))
    I_2 = np.exp(A * X_piL) * (-1j * np.pi - expi(-A * X_piL)) * np.exp(-Z)

    I_3 = np.exp(-A * L_1) * (1j * np.pi - expi(A * L_1, theta_b=np.pi))
    I_4 = (
        -np.exp(-A * X_piL) * (1j * np.pi - expi(A * X_piL, theta_b=np.pi)) * np.exp(-Z)
    )

    I_5 = -np.exp(A * L_2) * (expi(-A * L_2, theta_b=np.pi) + 1j * np.pi)
    I_6 = (
        np.exp(A * X_miL) * (expi(-A * X_miL, theta_b=np.pi) + 1j * np.pi) * np.exp(-Z)
    )

    I_7 = np.exp(-A * L_2) * (expi(A * L_2) + 1j * np.pi)
    I_8 = -np.exp(-A * X_miL) * (expi(A * X_miL) + 1j * np.pi) * np.exp(-Z)

    I = I_1 + I_2 + I_3 + I_4 + I_5 + I_6 + I_7 + I_8
    I_u = I_1 - I_2 - I_3 - I_4 - I_5 - I_6 + I_7 - I_8
    I_w = A * (-I_1 - I_2 + I_3 + I_4 - I_5 - I_6 + I_7 + I_8)
    psi = I * D * A
    u = I_u * D * A
    w = I_w * D * A

    fields_dict = {}
    fields_dict["psi"] = psi
    fields_dict["u"] = u
    fields_dict["w"] = w

    Q = 1 / np.pi * (np.pi / 2 + np.arctan(X / L)) * np.exp(-Z)
    fields_dict["Q"] = Q

    args = [u, w, f_omega, alpha_omega, fields]
    polarized_fields = recover_polarized_default(*args)
    fields_dict.update(polarized_fields)

    # phi TBD

    return fields_dict
