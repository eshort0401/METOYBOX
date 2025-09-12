"""
Classes for creating and managing interactive figures for browser deployment. Please see
_static/assets/js/model-controls.js for the names of the DOM elements we expect to
interact with.
"""

import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable

# from pyscript import document, display, when


def default_scalings():
    """Default scalings for re-dimensionalization."""
    x_star = lambda x, N, H, omega: x * (N / omega) * H
    z_star = lambda z, H: z * H
    psi_star = lambda psi, Q_0, H, N, omega: psi * (Q_0 * H / (N / omega))
    u_star = lambda u, Q_0, N, omega: u * (Q_0 / (N * omega))
    w_star = lambda w, Q_0, N: w * Q_0 / N


class WebCache:
    """Cache for DOM elements to avoid repeated lookups."""

    def __init__(self):
        self.elements = {}

    def get(self, element_id):
        if element_id not in self.elements:
            self.elements[element_id] = document.getElementById(element_id)
        return self.elements[element_id]


class BaseFieldProperties:
    """
    Base class to manage the properties of fields we need for visualization.
    """

    def __init__(
        self,
        name: str,
        label: str,
        field: NDArray[np.complex128],
        max: float = 1.0,
        min: float | None = None,
    ):
        """Initialize field properties."""
        self.name = name
        self.label = label
        self.field = field
        self.max = max
        if min is None:
            self.min = -np.abs(max)


class ScalarFieldProperties(BaseFieldProperties):
    """
    Class to manage the properties of scalar fields we need for visualization.

    Attributes:
        name (str): Name of the field (e.g., 'psi', 'u', 'w', 'Q').
        max (float): Maximum value for contourf levels.
        cmap_name (str): Colormap name for visualization.
    """

    def __init__(
        self,
        name: str,
        label: str,
        field: None | NDArray[np.complex128],
        max: float = 1.0,
        min: float | None = None,
        cmap_name: str = "RdBu_r",
    ):
        """Initialize field properties."""
        super().__init__(name, label, field, max, min)
        self.cmap = plt.get_cmap(cmap_name)
        self.levels = np.linspace(self.min, self.max, 21)
        _kwargs = {"ncolors": self.cmap.N, "extend": "both"}
        self.norm = mcolors.BoundaryNorm(self.levels, **_kwargs)


class VectorFieldProperties(BaseFieldProperties):
    """
    Class to manage the properties of vector fields we need for visualization.
    """

    def __init__(
        self,
        name: str,
        label: str,
        fields: None | dict[str, NDArray[np.complex128] | None],
        quiver_scale: float = 2.5,
        quiver_step: int = 20,
        quiver_key_magnitude: float = 0.2,
    ):
        self.name = name
        self.label = label
        self.fields = fields
        self.quiver_scale = quiver_scale
        self.quiver_step = quiver_step
        self.quiver_key_magnitude = quiver_key_magnitude


def _initialize_ax(ax, x_ticks, z_ticks, x_limits, z_limits):
    """Setup the ax."""
    ax.set_ylim(z_limits)
    ax.set_xlim(x_limits)
    ax.set_xticks(x_ticks)
    ax.set_yticks(z_ticks)
    x_ticklabels = [f"{val:.1f}" for val in x_ticks]
    z_ticklabels = [f"{val:.1f}" for val in z_ticks]
    ax.set_xticklabels(x_ticklabels)
    ax.set_yticklabels(z_ticklabels)
    ax.set_xlabel(r"$x$ [-]")
    ax.set_ylabel(r"$z$ [-]")


psi_properties = ScalarFieldProperties(
    "psi", r"$\psi$", None, max=1.0, cmap_name="RdBu_r"
)
velocity_properties = VectorFieldProperties(
    "velocity", r"$\mathbf{v}$", {"u": None, "w": None}
)


class BaseWaveModel:
    """Class for managing the visualization of wave models."""

    def __init__(
        self,
        name: str,
        x: NDArray[np.complex128],
        z: NDArray[np.complex128],
        x_ticks: NDArray[np.float64] | None,
        z_ticks: NDArray[np.float64] | None,
        x_limits: tuple[float, float] | None,
        z_limits: tuple[float, float] | None,
        figure_size: tuple[float] = (5, 4),
        suptitle_height: float = 1.0,
        field_properties: None | dict[str, BaseFieldProperties] = None,
    ):
        """Initialize the model."""
        self.name = name
        self.fig: plt.Figure = None
        self.ax: plt.Axes = None
        self.figure_size = figure_size
        self.suptitle_height = suptitle_height
        self.cache = WebCache()
        self.x, self.z, self.x_ticks, self.z_ticks = x, z, x_ticks, z_ticks
        self.x_limits, self.z_limits = x_limits, z_limits
        self.X: NDArray[np.complex128] = None
        self.Z: NDArray[np.complex128] = None
        self.X, self.Z = np.meshgrid(x, z)
        self.field_properties = field_properties
        self.active_imshow_field: str | None = None
        self.active_contour_field: str | None = None
        self.active_quiver_field: tuple[str, str] | None = None
        self.imshow, self.quiver, self.contour = None, None, None
        self.quiver_key, self.colorbar_ax, self.colorbar = None, None, None

    def initialize_figure(
        self, starting_imshow: str, starting_quiver: str, starting_contour: str = None
    ):
        """Initialize the figure with the fields."""

        # Initialize the figure, axes and layout
        self.fig, self.ax = plt.subplots(figsize=self.figure_size)
        self.fig.patch.set_facecolor("#E6E6E6")
        self.X, self.Z = np.meshgrid(self.x, self.z)
        args = [self.ax, self.x_ticks, self.z_ticks, self.x_limits, self.z_limits]
        _initialize_ax(*args)
        self.fig.suptitle("", y=self.suptitle_height)

        # Initialize the imshow
        imshow_properties = self.field_properties[starting_imshow]
        kwargs = {"cmap": imshow_properties.cmap, "norm": imshow_properties.norm}
        kwargs.update({"origin": "lower", "aspect": "auto", "zorder": 0})
        extent = [self.x.min(), self.x.max(), self.z.min(), self.z.max()]
        kwargs.update({"extent": extent, "norm": imshow_properties.norm})
        kwargs.update({"rasterized": True})
        dummy_data = np.ones_like(self.Z) * np.nan
        self.imshow = self.ax.imshow(dummy_data, **kwargs)
        divider = make_axes_locatable(self.ax)
        self.colorbar_ax = divider.append_axes("right", size="5.5%", pad=0.25)
        kwargs = {"cax": self.colorbar_ax, "extend": "both"}
        self.colorbar = self.fig.colorbar(self.imshow, **kwargs)

        # Initialize the quiver
        quiver_properties = self.field_properties[starting_quiver]
        step = quiver_properties.quiver_step
        quiver_scale = quiver_properties.quiver_scale
        subset = (slice(int(step / 2), None, step), slice(int(step / 2), None, step))
        args = [self.X[subset], self.Z[subset], dummy_data[subset], dummy_data[subset]]
        kwargs = {"color": "k", "scale": quiver_scale, "width": 0.006}
        kwargs.update({"angles": "xy", "zorder": 2, "rasterized": True})
        self.quiver = self.ax.quiver(*args, **kwargs)
        key_mag = quiver_properties.quiver_key_magnitude
        args = [self.quiver, 0.09, 1.05, key_mag, f"{key_mag} [-]"]
        kwargs = {"labelpos": "E", "coordinates": "axes"}
        self.quiver_key = self.ax.quiverkey(*args, **kwargs)

        # Initialize the contour
        # Not yet implemented

        # Initialize the displacements
        # Not yet implemented


def is_dimensional_mode():
    """Check if dimensional mode is active."""
    dim_radio = document.getElementById("dimensional-button")
    return dim_radio.checked if dim_radio else False
