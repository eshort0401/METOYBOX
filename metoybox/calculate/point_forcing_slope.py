import numpy as np
from typing import List
from numpy.typing import NDArray
from metoybox.calculate.utils import recover_polarized_default


def calculate_constants(f_omega, alpha_omega, N_omega, M):
    """Calculate the constants B, C, A, a_n, a_p used in the solution."""

    B = (
        (1 - 2 * 1j * alpha_omega - alpha_omega**2) * (1 + 1 / N_omega**2 * M**2)
        - f_omega**2
        - M**2
    ) ** (1 / 2)
    C = (1 / N_omega**2 * (-1 + 2 * 1j * alpha_omega + alpha_omega**2) + 1) ** (1 / 2)
    B, C = np.complex128(B), np.complex128(C)
    A = B / C
    g_1 = 1 / A * (-M / A + np.sqrt(M**2 / A**2 + 1))
    g_2 = 1 / A * (-M / A - np.sqrt(M**2 / A**2 + 1))

    if np.imag(g_1) > 0:
        g_p = g_1
        g_n = g_2
    else:
        g_p = g_2
        g_n = g_1

    return B, g_p, g_n


def calculate_fields_spatial(
    X: NDArray,
    Z: NDArray,
    M: float,
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

    B, g_p, g_n = calculate_constants(f_omega, alpha_omega, N_omega, M)

    D = 1j / (2 * np.pi * B**2 * (g_p - g_n))

    Z_sigma = Z - M * X
    mask = Z < M * X

    L_1 = g_p * Z_sigma - g_n * z_f + X
    L_2 = g_n * (Z_sigma - z_f) + X
    L_3 = g_p * (Z_sigma - z_f) + X
    L_4 = g_n * Z_sigma - g_p * z_f + X
    c_n = 1 - g_n * M
    c_p = 1 - g_p * M

    psi = D * (-c_n / L_1 + c_n / L_2 + c_p / L_3 - c_p / L_4)

    u = D * (
        c_n * g_p / L_1**2
        - c_n * g_n / L_2**2
        - c_p * g_p / L_3**2
        + c_p * g_n / L_4**2
    )
    w = -D * (
        c_n * (1 - g_p * M) / L_1**2
        - c_n * (1 - g_n * M) / L_2**2
        - c_p * (1 - g_p * M) / L_3**2
        + c_p * (1 - g_n * M) / L_4**2
    )

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

    sigma_hat = 1j + alpha_omega

    if "phi" in fields:
        phi = (
            -D
            * (sigma_hat + 1 / sigma_hat * f_omega**2)
            * (
                c_n * g_p / L_1 / (-g_p * M + 1)
                - c_n * g_n / L_2 / (-g_n * M + 1)
                - c_p * g_p / L_3 / (-g_p * M + 1)
                + c_p * g_n / L_4 / (-g_n * M + 1)
            )
        )
        fields_dict["phi"] = phi

    for key in fields_dict:
        # Mask values below the slope
        fields_dict[key][mask] = (1 + 1j) * np.nan

    return fields_dict
