import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.special import expi as sp_expi
from pyscript import document, display, when
import js


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


def initialize_figure():
    """Initialize the figure and set the global variables."""
    global fig, ax, im_psi, quiv, subset, x, z, psi_max
    global X, Z, psi_cbar, quiv_key

    # Create the grid offsetting by small amount to avoid singularity
    offset = 1e-8
    x = np.linspace(-4, 4 + offset, 201) - offset
    z = np.linspace(0, 8, 201)
    X, Z = np.meshgrid(x, z)

    fig, ax = plt.subplots(1, 1, figsize=(5, 4))
    fig.subplots_adjust(wspace=0.3)

    # Create placeholder artists.
    kwargs = {"cmap": "RdBu_r", "origin": "lower", "aspect": "auto", "zorder": 0}
    kwargs.update({"extent": [x.min(), x.max(), z.min(), z.max()]})
    cmap = plt.get_cmap(kwargs["cmap"])
    psi_max = 0.5
    psi_levels = np.linspace(-psi_max, psi_max, 21)
    psi_norm = mcolors.BoundaryNorm(psi_levels, ncolors=cmap.N, extend="both")

    im_psi = ax.imshow(np.zeros_like(Z), **kwargs, norm=psi_norm)
    psi_cbar = fig.colorbar(im_psi, ax=ax, extend="both")
    psi_cbar.set_label(r"$\psi$ [-]")
    psi_cbar.set_ticks(np.linspace(-psi_max, psi_max, 11))

    # Quiver plot
    step = 20
    subset = (slice(int(step / 2), None, step), slice(int(step / 2), None, step))
    dummy_wind = np.zeros_like(X)
    quiv_args = [X[subset], Z[subset], dummy_wind[subset], dummy_wind[subset]]
    quiv_kwargs = {"color": "k", "scale": 100, "width": 0.006, "angles": "xy"}
    quiv = ax.quiver(*quiv_args, **quiv_kwargs, zorder=2)
    kwargs = {"labelpos": "E", "coordinates": "axes"}
    quiv_key = ax.quiverkey(quiv, 0.95, 1.05, 10, r"10 [-]", **kwargs)

    ax.set_ylim(0, 8)
    ax.set_xlim(-4, 4)
    ax.set_xticks(np.arange(-4, 5, 2))
    ax.set_yticks(np.arange(0, 9, 2))
    ax.set_xlabel(r"$x$ [-]")
    ax.set_ylabel(r"$z$ [-]")
    ax.set_facecolor("tab:brown")
    ax.set_aspect("equal")

    ax.set_title(r"$\psi$ [-]")
    fig.patch.set_facecolor("#E6E6E6")
    fig.suptitle(r"", y=0.995)

    display(fig, target="plot-output")


def calculate_constants(f_omega, alpha_omega, N_omega):
    """Calculate the constants B, C, A, a_n, a_p used in the solution."""

    B = (-((1j + alpha_omega) ** 2) - f_omega**2) ** (1 / 2)
    C = (1 / (N_omega**2) * (1j + alpha_omega) ** 2 + 1) ** (1 / 2)
    B, C = np.complex128(B), np.complex128(C)
    A = B / C
    chi = np.sign(np.imag(1 / A))

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

    return D * (psi_1 + psi_2 + psi_3 + psi_4)


def amend_labels(event):
    """Amend the plot tick labels."""
    global psi_levels

    x_ticklabels = np.arange(-4, 5, 2)
    z_ticklabels = np.arange(0, 9, 2)
    psi_ticklabels = np.linspace(-psi_max, psi_max, 11)

    x_label = r"$x$ [-]"
    z_label = r"$z$ [-]"
    psi_label = r"$\psi$"

    quiv_label = r"$10$ [-]"

    checkbox = document.getElementById("dimensional_checkbox")
    if checkbox.checked:
        N_omega = float(document.getElementById("N_omega_slider").value)
        H = float(document.getElementById("H_slider").value)
        Q_0 = float(document.getElementById("Q_0_slider").value)
        omega = float(document.getElementById("omega_slider").value)
        x_ticklabels = x_ticklabels * N_omega * H / 1000  # km
        z_ticklabels = z_ticklabels * H / 1000  # km
        x_ticklabels = [f"{val:.2f}" for val in x_ticklabels]
        z_ticklabels = [f"{val:.2f}" for val in z_ticklabels]

        N = N_omega * omega
        psi_ticklabels = psi_ticklabels * Q_0 / (N * omega * H)
        scaled_psi_max = psi_max * Q_0 / (N * omega * H)
        exponent = int(np.floor(np.log10(scaled_psi_max)))

        psi_ticklabels = [f"{val/(10**exponent):.1f}" for val in psi_ticklabels]

        x_label = r"$x$ [km]"
        z_label = r"$z$ [km]"
        psi_label += rf" [$10^{{{exponent}}}$ m$^2$ s$^{{-1}}$]"

        u_key = 10 * Q_0 / (N * omega)
        w_key = 10 * Q_0 / (N**2)

        quiv_label = rf"$({u_key:0.1f} u, {w_key:0.1f} w)$ m s$^{{-1}}$"
    else:
        x_ticklabels = [f"{val:.2f}" for val in x_ticklabels]
        z_ticklabels = [f"{val:.2f}" for val in z_ticklabels]
        psi_ticklabels = [f"{val:.1f}" for val in psi_ticklabels]
        psi_label += r" [-]"

    ax.set_xticklabels(x_ticklabels)
    ax.set_yticklabels(z_ticklabels)
    psi_cbar.set_ticklabels(psi_ticklabels)
    ax.set_title(psi_label)

    ax.set_xlabel(x_label)
    ax.set_ylabel(z_label)
    psi_cbar.set_label(psi_label)

    quiv_key.text.set_text(quiv_label)

    update_suptitle(event)

    display(fig, target="plot-output", append=False)


@when("change", "#dimensional_checkbox")
def toggle_dimensional_controls(event):
    """Enable/disable dimensional controls based on checkbox state"""
    checkbox = document.getElementById("dimensional_checkbox")
    dimensional_elements = document.querySelectorAll(".dimensional-param")

    for element in dimensional_elements:
        if checkbox.checked:
            element.removeAttribute("disabled")
            element.classList.remove("disabled")
        else:
            element.setAttribute("disabled", "true")
            element.classList.add("disabled")

    amend_labels(checkbox)


dimensional_sliders = "#H_slider, #omega_slider, #Q_0_slider, #N_omega_slider"


@when("input", dimensional_sliders)
def update_dimensional_params(event):
    """Update dimensional parameters and recalculate dependent parameters."""
    # Get slider values
    H = float(document.getElementById("H_slider").value)
    omega = float(document.getElementById("omega_slider").value)
    Q_0 = float(document.getElementById("Q_0_slider").value)
    N_omega = float(document.getElementById("N_omega_slider").value)

    # Update the text output
    document.getElementById("H_out").innerText = f"{H/1000:.2f} km"
    document.getElementById("omega_out").innerText = rf"{omega:.2e} s⁻¹"
    document.getElementById("Q_0_out").innerText = rf"{Q_0:.2e} m s⁻³"
    document.getElementById("N_omega_out").innerText = f"{N_omega:.2f}"

    amend_labels(event)
    update_suptitle(event)


sliders = "#f_omega_slider, #alpha_omega_slider, #N_omega_slider, #t_slider"


@when("input", sliders)
def update_params(event):
    """Update the model parameters."""
    global psi_tilde, B, A, chi, u_tilde, w_tilde

    # Get slider values
    f_omega = float(document.getElementById("f_omega_slider").value)
    alpha_omega = float(document.getElementById("alpha_omega_slider").value)
    N_omega = float(document.getElementById("N_omega_slider").value)

    # Update the text output
    document.getElementById("f_omega_out").innerText = f"{f_omega:.2f}"
    document.getElementById("alpha_omega_out").innerText = f"{alpha_omega:.2f}"
    document.getElementById("N_omega_out").innerText = f"{N_omega:.2f}"

    # Perform the original physics calculations
    A, B, chi = calculate_constants(f_omega, alpha_omega, N_omega)
    psi_tilde = get_psi_tilde(X, Z, A, B, chi)

    update_time(event)


@when("input", "#t_slider")
def update_time(event):
    # Get slider values
    t = float(document.getElementById("t_slider").value)
    document.getElementById("t_out").innerText = f"{t:.2f}"

    psi = np.real(psi_tilde * np.exp(1j * t))
    # u = np.real(u_tilde * np.exp(1j * sigma * t))
    # w = np.real(w_tilde * np.exp(1j * sigma * t))

    # u[np.abs(u) > 15] = np.nan
    # w[np.abs(w) > 15] = np.nan

    # Update artist data
    im_psi.set_data(psi)
    # quiv.set_UVC(u[subset], w[subset])

    update_suptitle(event)

    # Redraw fig using display
    display(fig, target="plot-output", append=False)


def hide_loading_screen():
    """Hide loading screen and show main content"""
    loading_screen = document.getElementById("loading-screen")
    main_content = document.getElementById("main-content")

    loading_screen.style.display = "none"
    main_content.style.display = "block"


def update_suptitle(event):
    """Update the figure suptitle based on dimensional checkbox state."""
    t = float(document.getElementById("t_slider").value)
    checkbox = document.getElementById("dimensional_checkbox")
    if checkbox.checked:
        omega = float(document.getElementById("omega_slider").value)
        t_seconds = t / omega
        hour = int(np.floor(t_seconds / 3600))
        minute = int(np.floor((t_seconds - hour * 3600) / 60))
        second = int(t_seconds - hour * 3600 - minute * 60)
        time_str = f"{hour:02d}$ hr ${minute:02d}$ min ${second:.1f}$ s"
        fig.suptitle(rf"$t={time_str}", y=0.995)
    else:
        fig.suptitle(rf"$t={t/np.pi:.4f}\pi$ [-]", y=0.995)


initialize_figure()
update_params(None)
update_dimensional_params(None)
update_suptitle(None)
hide_loading_screen()
