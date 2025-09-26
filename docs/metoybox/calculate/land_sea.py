import numpy as np
from scipy.special import expi as sp_expi


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


def calculate_constants(f_omega, alpha_omega, N_omega):
    """Calculate the constants B, C, A, a_n, a_p used in the solution."""

    B = (-((1j + alpha_omega) ** 2) - f_omega**2) ** (1 / 2)
    C = (1 / (N_omega**2) * (1j + alpha_omega) ** 2 + 1) ** (1 / 2)
    B, C = np.complex128(B), np.complex128(C)
    A = B / C
    chi = np.sign(np.imag(1 / A))
    # Choose the correct branch for chi
    if chi < 0:
        chi = chi * np.exp(1j * np.pi)

    return A, B, chi


def get_psi_tilde(X, Z, A, B, chi):
    """Get the psi_p_tilde solution."""

    L_1 = chi * (1 / A) * Z + X
    L_2 = -chi * (1 / A) * Z + X

    psi_1 = np.zeros_like(Z, dtype=complex)
    psi_2 = np.zeros_like(Z, dtype=complex)
    psi_3 = np.zeros_like(Z, dtype=complex)
    psi_4 = np.zeros_like(Z, dtype=complex)

    D = -1 / (B**2 * 4 * np.pi * 1j)

    psi_1 += -np.exp(A * L_1) * (-1j * np.pi - expi(-A * L_1))
    psi_1 += np.exp(A * X) * (-1j * np.pi - expi(-A * X)) * np.exp(-Z)

    psi_1 += np.exp(-A * L_1) * (1j * np.pi - expi(A * L_1, theta_b=np.pi))
    psi_1 += -np.exp(-A * X) * (1j * np.pi - expi(A * X, theta_b=np.pi)) * np.exp(-Z)

    psi_1 += -np.exp(A * L_2) * (expi(-A * L_2, theta_b=np.pi) + 1j * np.pi)
    psi_1 += np.exp(A * X) * (expi(-A * X, theta_b=np.pi) + 1j * np.pi) * np.exp(-Z)

    psi_1 += np.exp(-A * L_2) * (expi(A * L_2) + 1j * np.pi)
    psi_1 += -np.exp(-A * X) * (expi(A * X) + 1j * np.pi) * np.exp(-Z)

    return D * A * (psi_1 + psi_2 + psi_3 + psi_4)
