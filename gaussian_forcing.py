import asyncio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pyscript import document, display, when
import js


def initialize_figure():
    """Initialize the figure and set the global variables."""
    global fig, ax, im_psi, quiv, subset, x, z, psi_max
    global X, Z

    x = np.linspace(-1, 1, 201)
    z = np.linspace(0, 2, 401)
    X, Z = np.meshgrid(x, z)

    fig, ax = plt.subplots(1, 1, figsize=(5, 4))
    fig.subplots_adjust(wspace=0.3)

    # Create placeholder artists.
    kwargs = {"cmap": "RdBu_r", "origin": "lower", "aspect": "auto", "zorder": 0}
    kwargs.update({"extent": [x.min(), x.max(), z.min(), z.max()]})
    cmap = plt.get_cmap(kwargs["cmap"])
    psi_max = 4.0
    psi_levels = np.linspace(-psi_max, psi_max, 21)
    psi_norm = mcolors.BoundaryNorm(psi_levels, ncolors=cmap.N, extend="both")

    im_psi = ax.imshow(np.zeros_like(Z), **kwargs, norm=psi_norm)
    psi_cbar = fig.colorbar(im_psi, ax=ax, extend="both")
    psi_cbar.set_label(r"$\psi$ [-]")
    psi_cbar.set_ticks(np.linspace(-psi_max, psi_max, 11))

    # # Quiver plot
    # step = 20
    # subset = (slice(None, None, step), slice(None, None, step))
    # dummy_wind = np.zeros_like(X)
    # quiv_args = [X[subset], Z[subset], dummy_wind[subset], dummy_wind[subset]]
    # quiv_kwargs = {"color": "k", "scale": 2.5, "width": 0.006, "angles": "xy"}
    # quiv = axes[0].quiver(*quiv_args, **quiv_kwargs, zorder=2)
    # axes[0].quiverkey(
    #     quiv, 0.80, 1.05, 0.2, r"0.2 [-]", labelpos="E", coordinates="axes"
    # )

    ax.set_ylim(0, 2)
    ax.set_xlim(-1, 1)
    ax.set_xticks(np.arange(-1, 1.5, 0.5))
    ax.set_yticks(np.arange(0, 2.5, 0.5))
    ax.set_xlabel(r"$x$ [-]")
    ax.set_ylabel(r"$z$ [-]")
    ax.set_facecolor("tab:brown")
    ax.set_aspect("equal")

    ax.set_title(r"$\operatorname{Re}\left\{\widetilde{\psi}e^{i\sigma t}\right\}$ [-]")
    fig.patch.set_facecolor("#E6E6E6")
    fig.suptitle(r"", y=0.995)

    display(fig, target="plot-output")


def calculate_constants(f_omega, alpha_omega, N_omega, sigma):
    """Calculate the constants B, C, A, a_n, a_p used in the solution."""

    B = (-((1j * sigma + alpha_omega) ** 2) - f_omega**2) ** (1 / 2)
    C = (1 / (N_omega**2) * (1j * sigma + alpha_omega) ** 2 + 1) ** (1 / 2)
    B, C = np.complex128(B), np.complex128(C)
    A = B / C
    chi = np.sign(np.imag(1 / A))

    return A, B, chi


def get_psi_tilde(X, Z, z_f, A, B, sigma, chi):
    """Get the psi_p_tilde solution."""

    cond_1 = Z <= z_f
    cond_2 = Z > z_f

    psi_tilde = np.zeros_like(Z, dtype=complex)

    t_1 = chi * z_f + Z[cond_1]
    t_2 = chi * z_f - Z[cond_1]
    t_3 = -t_2
    t_4 = -t_1

    D = 1j * A * np.exp(-(sigma**2) / 4) / (4 * np.sqrt(np.pi) * B**2)

    psi_tilde[cond_1] = D * (
        -1 / (1 / A * t_1 + X[cond_1])
        + 1 / (1 / A * t_2 + X[cond_1])
        + 1 / (1 / A * t_3 + X[cond_1])
        - 1 / (1 / A * t_4 + X[cond_1])
    )

    t_1 = z_f + chi * Z[cond_2]
    t_2 = -z_f + chi * Z[cond_2]
    t_3 = -t_2
    t_4 = -t_1

    psi_tilde[cond_2] = D * (
        -1 / (1 / A * t_1 + X[cond_2])
        + 1 / (1 / A * t_2 + X[cond_2])
        + 1 / (1 / A * t_3 + X[cond_2])
        - 1 / (1 / A * t_4 + X[cond_2])
    )

    return psi_tilde


# In your Python code (gaussian_forcing.py)
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

    # Amend ticklabels
    x_ticklabels = np.arange(-1, 1.5, 0.5)
    z_ticklabels = np.arange(0, 2.5, 0.5)
    x_label = r"$x$ [-]"
    z_label = r"$z$ [-]"
    if checkbox.checked:
        N_omega = float(document.getElementById("N_omega_slider").value)
        H = float(document.getElementById("H_slider").value)
        x_ticklabels = x_ticklabels * N_omega * H / 1000  # km
        z_ticklabels = z_ticklabels * H / 1000  # km
        x_label = r"$x$ [km]"
        z_label = r"$z$ [km]"

    # Ensure labels rounded to two decimal places
    x_ticklabels = [f"{val:.2f}" for val in x_ticklabels]
    z_ticklabels = [f"{val:.2f}" for val in z_ticklabels]
    ax.set_xticklabels(x_ticklabels)
    ax.set_yticklabels(z_ticklabels)
    ax.set_xlabel(x_label)
    ax.set_ylabel(z_label)

    display(fig, target="plot-output", append=False)


# Initialize the state (disabled by default)
# toggle_dimensional_controls(None)


sliders = "#f_omega_slider, #alpha_omega_slider, #N_omega_slider, "
sliders += "#z_f_slider, #t_slider, #sigma_slider"


@when("input", sliders)
def update_params(event):
    """Update the model parameters."""
    global psi_tilde, B, A, chi

    # Get slider values
    f_omega = float(document.getElementById("f_omega_slider").value)
    alpha_omega = float(document.getElementById("alpha_omega_slider").value)
    N_omega = float(document.getElementById("N_omega_slider").value)
    sigma = float(document.getElementById("sigma_slider").value)
    z_f = float(document.getElementById("z_f_slider").value)

    # Update the text output
    document.getElementById("f_omega_out").innerText = f"{f_omega:.2f}"
    document.getElementById("alpha_omega_out").innerText = f"{alpha_omega:.2f}"
    document.getElementById("N_omega_out").innerText = f"{N_omega:.1f}"
    document.getElementById("sigma_out").innerText = f"{sigma:.2f}"
    document.getElementById("z_f_out").innerText = f"{z_f:.2f}"

    # Perform the original physics calculations
    A, B, chi = calculate_constants(f_omega, alpha_omega, N_omega, sigma)
    psi_tilde = get_psi_tilde(X, Z, z_f, A, B, sigma, chi)

    update_time(event)


@when("input", "#t_slider")
def update_time(event):
    # Get slider values
    t = float(document.getElementById("t_slider").value)
    sigma = float(document.getElementById("sigma_slider").value)
    document.getElementById("t_out").innerText = f"{t:.2f}"

    psi = np.real(psi_tilde * np.exp(1j * sigma * t))

    # Update artist data
    im_psi.set_data(psi)

    fig.suptitle(rf"$t={t/np.pi:.4f}\pi$ [-]", y=0.995)

    # Redraw fig using display
    display(fig, target="plot-output", append=False)


def hide_loading_screen():
    """Hide loading screen and show main content"""
    loading_screen = document.getElementById("loading-screen")
    main_content = document.getElementById("main-content")

    loading_screen.style.display = "none"
    main_content.style.display = "block"


initialize_figure()
update_params(None)
hide_loading_screen()
