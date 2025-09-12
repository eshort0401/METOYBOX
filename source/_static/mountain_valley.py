import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pyscript import document, display, when
import js


omega = 2 * np.pi / (24 * 3600)
suptitle_height = 1.0


class WebCache:
    """Cache for DOM elements to avoid repeated lookups."""

    def __init__(self):
        self.elements = {}

    def get(self, element_id):
        if element_id not in self.elements:
            self.elements[element_id] = document.getElementById(element_id)
        return self.elements[element_id]


# Create cache once
cache = WebCache()


def is_dimensional_mode():
    """Check if dimensional mode is active."""
    dim_radio = document.getElementById("dimensional-button")
    return dim_radio.checked if dim_radio else False


@when("change", "#dimensional-button, #non-dimensional-button")
def on_coordinate_change(event):
    """Handle coordinate system changes"""
    if is_dimensional_mode():
        update_dimensional_params(event)
    else:
        update_params(event)
    amend_labels(event)


dimensional_sliders = "#H-slider, #Q0-slider, #N-slider"


@when("input", dimensional_sliders)
def update_dimensional_params(event):
    """Update dimensional parameters and recalculate dependent parameters."""
    amend_labels(event)
    update_suptitle(event)


def initialize_figure():
    """Initialize the figure and set the global variables."""
    global fig, ax, im_psi, quiv, slope_line_psi, subset, x, z
    global X, Z, psi_cbar, quiv_key, psi_levels, psi_max, ax, quiv_key_mag

    x = np.linspace(-2, 2, 201)
    z = np.linspace(-1, 4, 401)
    X, Z = np.meshgrid(x, z)

    fig, ax = plt.subplots(1, 1, figsize=(5, 4))
    fig.subplots_adjust(wspace=0.3)

    # Create placeholder artists.
    kwargs = {"cmap": "RdBu_r", "origin": "lower", "aspect": "auto", "zorder": 0}
    kwargs.update({"extent": [x.min(), x.max(), z.min(), z.max()]})
    cmap = plt.get_cmap(kwargs["cmap"])
    # Q_levels = np.linspace(-1, 1, 21)
    # Q_norm = mcolors.BoundaryNorm(Q_levels, ncolors=cmap.N, extend="both")
    psi_max = 0.5
    psi_levels = np.linspace(-psi_max, psi_max, 21)
    psi_norm = mcolors.BoundaryNorm(psi_levels, ncolors=cmap.N, extend="both")

    # Plot psi
    im_psi = ax.imshow(np.zeros_like(Z), **kwargs, norm=psi_norm, rasterized=True)
    divider = make_axes_locatable(ax)
    cbar_ax = divider.append_axes("right", size="5.5%", pad=0.25)
    psi_cbar = fig.colorbar(im_psi, cax=cbar_ax, extend="both")
    psi_cbar.set_label(r"$\psi$ [-]")
    psi_cbar.set_ticks(np.linspace(-psi_max, psi_max, 11))

    # Plot Q
    # im_Q = axes[1].imshow(np.zeros_like(Z), **kwargs, norm=Q_norm, rasterized=True)
    # Q_cbar = fig.colorbar(im_Q, ax=axes[1], extend="both")
    # Q_cbar.set_label(r"$Q$ [-]")
    # Q_cbar.set_ticks(np.linspace(-1, 1, 11))

    # Quiver plot
    step = 20
    subset = (slice(int(step / 2), None, step), slice(int(step / 2), None, step))
    dummy_wind = np.zeros_like(X)
    quiv_args = [X[subset], Z[subset], dummy_wind[subset], dummy_wind[subset]]
    quiv_kwargs = {"color": "k", "scale": 2.5, "width": 0.006, "angles": "xy"}
    quiv = ax.quiver(*quiv_args, **quiv_kwargs, zorder=2, rasterized=True)
    quiv_key_mag = 0.2
    args = [quiv, 0.09, 1.05, quiv_key_mag, rf"{quiv_key_mag} [-]"]
    kwargs = {"labelpos": "E", "coordinates": "axes"}
    quiv_key = ax.quiverkey(*args, **kwargs)

    # Plot the slope line
    dark_brown = tuple([c * 0.5 for c in mcolors.to_rgb("tab:brown")])
    slope_line_psi = ax.plot(x, x * 0, color=dark_brown, zorder=1)[0]
    # slope_line_Q = ax.plot(x, x * 0, color=dark_brown, zorder=1)[0]

    ax.set_ylim(-1, 3)
    ax.set_xlim(-2, 2)
    ax.set_xticks(np.arange(-2, 3, 1))
    ax.set_yticks(np.arange(-1, 4, 1))
    x_ticklabels = [f"{val:.1f}" for val in np.arange(-2, 3, 1)]
    z_ticklabels = [f"{val:.1f}" for val in np.arange(-1, 4, 1)]
    ax.set_xticklabels(x_ticklabels)
    ax.set_yticklabels(z_ticklabels)
    ax.set_xlabel(r"$x$ [-]")
    ax.set_ylabel(r"$z$ [-]")
    ax.set_facecolor("tab:brown")
    ax.set_aspect("equal")

    fig.patch.set_facecolor("#E6E6E6")
    # fig.tight_layout()
    fig.suptitle(r"", y=suptitle_height)

    # Display the empty figure template on the page immediately
    display(fig, target="plot-output", append=False)


def update_suptitle(event):
    """Update the figure suptitle based on dimensional state."""
    t = float(document.getElementById("t-slider").value)
    if is_dimensional_mode():
        t_seconds = t / omega
        hour = int(np.floor(t_seconds / 3600))  # note t=0 is noon
        hour_LST = int((hour + 12) % 24)  # convert to LST
        minute = int(np.floor((t_seconds - hour * 3600) / 60))
        second = int(np.round(t_seconds - hour * 3600 - minute * 60))
        time_str = f"{hour_LST:02d}:{minute:02d}:{second:02d}"
        fig.suptitle(rf"{time_str} [LST]", y=suptitle_height)
    else:
        fig.suptitle(rf"$t={t:.2f}$ [-]", y=suptitle_height)


def amend_labels(event):
    """Amend the plot tick labels."""
    global psi_levels

    x_ticklabels = np.arange(-2, 3, 1)
    z_ticklabels = np.arange(-1, 4, 1)

    psi_ticklabels = np.linspace(-psi_max, psi_max, 11)

    x_label = r"$x$ [-]"
    z_label = r"$z$ [-]"
    psi_label = r"$\psi$"
    Q_label = r"$Q$"

    quiv_label = rf"{quiv_key_mag} [-]"

    if is_dimensional_mode():
        H = float(document.getElementById("H-slider").value)
        Q_0 = float(document.getElementById("Q0-slider").value)
        N = float(document.getElementById("N-slider").value)
        x_ticklabels = x_ticklabels * (N / omega) * H / 1000  # km
        z_ticklabels = z_ticklabels * H / 1000  # km
        x_ticklabels = [f"{val:.1f}" for val in x_ticklabels]
        z_ticklabels = [f"{val:.1f}" for val in z_ticklabels]

        psi_max_dim = Q_0 * H / (N * omega) * psi_max
        exp = int(np.floor(np.log10(psi_max_dim)))
        psi_ticklabels = psi_ticklabels * Q_0 * H / (N * omega)
        if exp < -1 or exp > 2:
            psi_ticklabels = psi_ticklabels * 10 ** (-exp)
            psi_label += rf" [$10^{{{exp}}}$ m$^2$ s$^{{-1}}$]"
        else:
            psi_label += rf" [m$^2$ s$^{{-1}}$]"

        psi_ticklabels = [f"{val:.1f}" for val in psi_ticklabels]

        x_label = r"$x$ [km]"
        z_label = r"$z$ [km]"
        Q_label += r" [m s$^{-3}$]"

        u_key = quiv_key_mag * Q_0 / (N * omega)
        w_key = quiv_key_mag * Q_0 / (N**2)

        quiv_label = rf"$u:$ ${u_key:0.1f}$ m s$^{{-1}}$, "
        quiv_label += rf"$w:$ ${w_key*100:0.1f}$ cm s$^{{-1}}$"
    else:
        x_ticklabels = [f"{val:.1f}" for val in x_ticklabels]
        z_ticklabels = [f"{val:.1f}" for val in z_ticklabels]
        psi_ticklabels = [f"{val:.1f}" for val in psi_ticklabels]
        psi_label += r" [-]"
        Q_label += r" [-]"

    ax.set_xticklabels(x_ticklabels)
    ax.set_yticklabels(z_ticklabels)
    ax.set_xlabel(x_label)
    ax.set_ylabel(z_label)
    psi_cbar.set_ticklabels(psi_ticklabels)
    psi_cbar.set_label(psi_label)

    quiv_key.text.set_text(quiv_label)

    update_suptitle(event)

    display(fig, target="plot-output", append=False)


def get_parameters():
    """Get the non-dimensional parameters from the appropriate sliders."""

    if is_dimensional_mode():
        f = float(cache.get("f-slider").value)
        alpha = float(cache.get("alpha-slider").value)
        N = float(cache.get("N-slider").value)
        M_dim = float(cache.get("M-dim-slider").value)
        f_omega = f / omega
        alpha_omega = alpha / omega
        N_omega = N / omega
        M = M_dim * N / omega
    else:
        f_omega = float(cache.get("f-omega-slider").value)
        alpha_omega = float(cache.get("alpha-omega-slider").value)
        N_omega = float(cache.get("N-omega-slider").value)
        M = float(cache.get("M-slider").value)

    return f_omega, alpha_omega, N_omega, M


def update_outputs():
    """Update the output text elements with current parameter values."""

    if is_dimensional_mode():
        for name in ["f", "alpha", "N", "M-dim"]:
            value = float(cache.get(f"{name}-slider").value)
            out = cache.get(f"{name}-out")
            out.textContent = f"{value:.1e}" + f" {out.units}"
    else:
        for name in ["f-omega", "alpha-omega", "N-omega", "M"]:
            value = float(cache.get(f"{name}-slider").value)
            out = cache.get(f"{name}-out")
            out.textContent = f"{value:.2f}" + f" {out.units}"


parameter_sliders = "#f-omega-slider, #alpha-omega-slider, #N-omega-slider, #M-slider, "
parameter_sliders += "#f-slider, #alpha-slider, #N-slider, #M-dim-slider"


@when("input", parameter_sliders)
def update_params(event):
    """Update the model parameters."""
    global psi_base, u_base, w_base, Q_base, B

    update_outputs()
    f_omega, alpha_omega, N_omega, M = get_parameters()

    Z_sigma = Z - M * X
    B = (
        (1 - 2j * alpha_omega - alpha_omega**2) * (1 + (1 / N_omega**2) * M**2)
        - f_omega**2
        - M**2
    ) ** 0.5
    abs_B_sq = np.abs(B) ** 2
    exp_Z = np.exp(-Z_sigma)

    psi_base = M / abs_B_sq * (exp_Z - 1)
    u_base = -M / abs_B_sq * exp_Z
    w_base = -(M**2) / abs_B_sq * exp_Z
    Q_base = exp_Z

    mask = Z < M * X
    psi_base[mask] = np.nan
    u_base[mask] = np.nan
    w_base[mask] = np.nan
    Q_base[mask] = np.nan

    update_time(event)


@when("input", "#t-slider, #t-dim-slider")
def update_time(event):
    # Get slider values
    if is_dimensional_mode():
        t_dim = float(cache.get("t-dim-slider").value)
        M_dim = float(cache.get("M-dim-slider").value)
        N = float(cache.get("N-slider").value)
        t = t_dim * omega
        M = M_dim * N / omega
        t_dim_out = cache.get("t-dim-out")
        t_dim_out.innerText = f"{t_dim:.2f}" + f" {t_dim_out.units}"
    else:
        t = float(cache.get("t-slider").value)
        M = float(cache.get("M-slider").value)

    t_out = cache.get("t-out")
    t_out.innerText = f"{t:.2f}" + f" {t_out.units}"

    cos_t_B = np.cos(t - 2 * np.angle(B))
    psi = psi_base * cos_t_B
    # Q = Q_base * np.cos(t)
    u = u_base * cos_t_B
    w = w_base * cos_t_B

    # Update artist data
    im_psi.set_data(psi)
    # im_Q.set_data(Q)
    slope_line_psi.set_ydata(x * M)  # this is always in non-dim coordinates
    # slope_line_Q.set_ydata(x * M)
    quiv.set_UVC(u[subset], w[subset])

    fig.suptitle(rf"$t={t:.2f}$ [-]", y=suptitle_height)

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
