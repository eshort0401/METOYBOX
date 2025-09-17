import asyncio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pyscript import document, display, when
import js


def initialize_figure():
    """Initialize the figure and set the global variables."""
    global fig, ax, im_psi, quiv, subset, x, z, psi_max
    global X, Z, psi_cbar, quiv_key

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

    # Quiver plot
    step = 20
    subset = (slice(int(step / 2), None, step), slice(int(step / 2), None, step))
    dummy_wind = np.zeros_like(X)
    quiv_args = [X[subset], Z[subset], dummy_wind[subset], dummy_wind[subset]]
    quiv_kwargs = {"color": "k", "scale": 100, "width": 0.006, "angles": "xy"}
    quiv = ax.quiver(*quiv_args, **quiv_kwargs, zorder=2)
    kwargs = {"labelpos": "E", "coordinates": "axes"}
    quiv_key = ax.quiverkey(quiv, 0.95, 1.05, 10, r"10 [-]", **kwargs)

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

    display(fig, target="figure-output")


def calculate_constants(f_omega, alpha_omega, N_omega, sigma):
    """Calculate the constants B, C, A, a_n, a_p used in the solution."""

    B = (-((1j * sigma + alpha_omega) ** 2) - f_omega**2) ** (1 / 2)
    C = (1 / (N_omega**2) * (1j * sigma + alpha_omega) ** 2 + 1) ** (1 / 2)
    B, C = np.complex128(B), np.complex128(C)
    A = B / C
    chi = np.sign(np.imag(1 / A))

    return A, B, chi


def get_psi_u_w_tilde(X, Z, z_f, A, B, sigma, chi):
    """Get the psi_p_tilde solution."""

    cond_1 = Z <= z_f
    cond_2 = Z > z_f

    psi_tilde = np.zeros_like(Z, dtype=complex)
    u_tilde = np.zeros_like(Z, dtype=complex)
    w_tilde = np.zeros_like(Z, dtype=complex)

    t_1 = 1 / A * (chi * z_f + Z[cond_1])
    t_2 = 1 / A * (chi * z_f - Z[cond_1])
    t_3 = -t_2
    t_4 = -t_1

    t_1 += X[cond_1]
    t_2 += X[cond_1]
    t_3 += X[cond_1]
    t_4 += X[cond_1]

    D = 1j * A * np.exp(-(sigma**2) / 4) / (4 * np.sqrt(np.pi) * B**2)

    psi_tilde[cond_1] = D * (-1 / t_1 + 1 / t_2 + 1 / t_3 - 1 / t_4)
    u_tilde[cond_1] = (D / A) * (1 / t_1**2 + 1 / t_2**2 - 1 / t_3**2 - 1 / t_4**2)
    w_tilde[cond_1] = -D * (1 / t_1**2 - 1 / t_2**2 - 1 / t_3**2 + 1 / t_4**2)

    t_1 = 1 / A * (z_f + chi * Z[cond_2])
    t_2 = 1 / A * (-z_f + chi * Z[cond_2])
    t_3 = -t_2
    t_4 = -t_1

    t_1 += X[cond_2]
    t_2 += X[cond_2]
    t_3 += X[cond_2]
    t_4 += X[cond_2]

    psi_tilde[cond_2] = D * (-1 / t_1 + 1 / t_2 + 1 / t_3 - 1 / t_4)
    u_tilde[cond_2] = (D / A * chi) * (
        1 / t_1**2 - 1 / t_2**2 + 1 / t_3**2 - 1 / t_4**2
    )
    w_tilde[cond_2] = -D * (1 / t_1**2 - 1 / t_2**2 - 1 / t_3**2 + 1 / t_4**2)

    return psi_tilde, u_tilde, w_tilde


def update_labels(event):
    """Amend the plot tick labels."""
    global psi_levels

    x_ticklabels = np.arange(-1, 1.5, 0.5)
    z_ticklabels = np.arange(0, 2.5, 0.5)
    psi_ticklabels = np.linspace(-psi_max, psi_max, 11)

    x_label = r"$x$ [-]"
    z_label = r"$z$ [-]"
    psi_label = r"$\operatorname{Re}\left\{\widetilde{\psi}e^{i\sigma t}\right\}$"

    quiv_label = r"$10$ [-]"

    checkbox = document.getElementById("dimensional_checkbox")
    if checkbox.checked:
        N_omega = float(document.getElementById("N-omega-slider").value)
        H = float(document.getElementById("H-slider").value)
        Q_0 = float(document.getElementById("Q0-slider").value)
        omega = float(document.getElementById("omega-slider").value)
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

    display(fig, target="figure-output", append=False)


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

    update_labels(checkbox)


dimensional_sliders = "#H-slider, #omega-slider, #Q0-slider, #N-omega-slider"


@when("input", dimensional_sliders)
def update_dimensional_params(event):
    """Update dimensional parameters and recalculate dependent parameters."""
    # Get slider values
    H = float(document.getElementById("H-slider").value)
    omega = float(document.getElementById("omega-slider").value)
    Q_0 = float(document.getElementById("Q0-slider").value)
    N_omega = float(document.getElementById("N-omega-slider").value)

    # Update the text output
    document.getElementById("H-out").innerText = f"{H/1000:.2f} km"
    document.getElementById("omega-out").innerText = rf"{omega:.2e} s⁻¹"
    document.getElementById("Q0-out").innerText = rf"{Q_0:.2e} m s⁻³"
    document.getElementById("N-omega-out").innerText = f"{N_omega:.2f}"

    update_labels(event)
    update_suptitle(event)


sliders = "#f-omega-slider, #alpha-omega-slider, #N-omega-slider, "
sliders += "#zf-slider, #t-slider, #sigma-slider"


@when("input", sliders)
def update_params(event):
    """Update the model parameters."""
    global psi_tilde, B, A, chi, u_tilde, w_tilde

    # Get slider values
    f_omega = float(document.getElementById("f-omega-slider").value)
    alpha_omega = float(document.getElementById("alpha-omega-slider").value)
    N_omega = float(document.getElementById("N-omega-slider").value)
    sigma = float(document.getElementById("sigma-slider").value)
    z_f = float(document.getElementById("zf-slider").value)

    # Update the text output
    document.getElementById("f-omega-out").innerText = f"{f_omega:.2f}"
    document.getElementById("alpha-omega-out").innerText = f"{alpha_omega:.2f}"
    document.getElementById("N-omega-out").innerText = f"{N_omega:.2f}"
    document.getElementById("sigma-out").innerText = f"{sigma:.2f}"
    document.getElementById("zf-out").innerText = f"{z_f:.2f}"

    # Perform the original physics calculations
    A, B, chi = calculate_constants(f_omega, alpha_omega, N_omega, sigma)
    psi_tilde, u_tilde, w_tilde = get_psi_u_w_tilde(X, Z, z_f, A, B, sigma, chi)

    update_time(event)


@when("input", "#t-slider")
def update_time(event):
    # Get slider values
    t = float(document.getElementById("t-slider").value)
    sigma = float(document.getElementById("sigma-slider").value)
    document.getElementById("t-out").innerText = f"{t:.2f}"

    psi = np.real(psi_tilde * np.exp(1j * sigma * t))
    u = np.real(u_tilde * np.exp(1j * sigma * t))
    w = np.real(w_tilde * np.exp(1j * sigma * t))

    u[np.abs(u) > 15] = np.nan
    w[np.abs(w) > 15] = np.nan

    # Update artist data
    im_psi.set_data(psi)
    quiv.set_UVC(u[subset], w[subset])

    update_suptitle(event)

    # Redraw fig using display
    display(fig, target="figure-output", append=False)


def hide_loading_screen():
    """Hide loading screen and show main content"""
    loading_screen = document.getElementById("loading-screen")
    main_content = document.getElementById("main-content")

    loading_screen.style.display = "none"
    main_content.style.display = "block"


def update_suptitle(event):
    """Update the figure suptitle based on dimensional checkbox state."""
    t = float(document.getElementById("t-slider").value)
    checkbox = document.getElementById("dimensional_checkbox")
    if checkbox.checked:
        omega = float(document.getElementById("omega-slider").value)
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
