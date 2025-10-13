import numpy as np
from typing import List
from numpy.typing import NDArray
from metoybox.calculate.utils import recover_polarized_default


def calculate_constants(f_omega, alpha_omega, N_omega, sigma):
    """Calculate the constants B, C, A, a_n, a_p used in the solution."""

    B = (-((1j * sigma + alpha_omega) ** 2) - f_omega**2) ** (1 / 2)
    C = (1 / (N_omega**2) * (1j * sigma + alpha_omega) ** 2 + 1) ** (1 / 2)
    B, C = np.complex128(B), np.complex128(C)
    A = B / C

    if np.imag(1 / A) < 0:
        A = -A

    return A, B


def calculate_fields_spatial(
    X: NDArray,
    Z: NDArray,
    z_f: float,
    sigma: float,
    f_omega: float,
    alpha_omega: float,
    N_omega: float,
    fields: List[str] = ["psi", "u", "w"],
):
    """Get the psi_p_tilde solution."""

    cond_1 = Z <= z_f
    cond_2 = Z > z_f

    psi = np.zeros_like(Z, dtype=complex)
    u = np.zeros_like(Z, dtype=complex)
    w = np.zeros_like(Z, dtype=complex)
    sigma_hat = 1j * sigma + alpha_omega
    phi = np.zeros_like(Z, dtype=complex)

    A, B = calculate_constants(f_omega, alpha_omega, N_omega, sigma)

    t_1 = 1 / A * (z_f + Z[cond_1])
    t_2 = 1 / A * (z_f - Z[cond_1])
    t_3 = -t_2
    t_4 = -t_1

    t_1 += X[cond_1]
    t_2 += X[cond_1]
    t_3 += X[cond_1]
    t_4 += X[cond_1]

    D = 1j * A * np.exp(-(sigma**2) / 4) / (4 * np.sqrt(np.pi) * B**2)

    psi[cond_1] = D * (-1 / t_1 + 1 / t_2 + 1 / t_3 - 1 / t_4)
    u[cond_1] = (D / A) * (1 / t_1**2 + 1 / t_2**2 - 1 / t_3**2 - 1 / t_4**2)
    w[cond_1] = -D * (1 / t_1**2 - 1 / t_2**2 - 1 / t_3**2 + 1 / t_4**2)
    A_phi = -(sigma_hat + f_omega**2 / sigma_hat) * D / A
    phi[cond_1] = A_phi * (-1 / t_1 - 1 / t_2 + 1 / t_3 + 1 / t_4)

    t_1 = 1 / A * (z_f + Z[cond_2])
    t_2 = 1 / A * (-z_f + Z[cond_2])
    t_3 = -t_2
    t_4 = -t_1

    t_1 += X[cond_2]
    t_2 += X[cond_2]
    t_3 += X[cond_2]
    t_4 += X[cond_2]

    psi[cond_2] = D * (-1 / t_1 + 1 / t_2 + 1 / t_3 - 1 / t_4)
    u[cond_2] = (D / A) * (1 / t_1**2 - 1 / t_2**2 + 1 / t_3**2 - 1 / t_4**2)
    w[cond_2] = -D * (1 / t_1**2 - 1 / t_2**2 - 1 / t_3**2 + 1 / t_4**2)
    phi[cond_2] = A_phi * (-1 / t_1 + 1 / t_2 - 1 / t_3 + 1 / t_4)

    fields_dict = {}
    fields_dict["psi"] = psi
    fields_dict["u"] = u
    fields_dict["w"] = w

    args = [u, w, f_omega, alpha_omega, fields]
    polarized_fields = recover_polarized_default(*args)
    fields_dict.update(polarized_fields)

    if "phi" in fields:
        fields_dict["phi"] = phi

    return fields_dict
