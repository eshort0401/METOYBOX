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
from pyscript import document, display, when


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
        field: NDArray[np.complex128],
        max: float = 1.0,
        min: float | None = None,
    ):
        """Initialize field properties."""
        self.name = name
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
        field: None | NDArray[np.complex128],
        max: float = 1.0,
        min: float | None = None,
        cmap_name: str = "RdBu_r",
    ):
        """Initialize field properties."""
        super().__init__(name, field, max, min)
        self.cmap = plt.get_cmap(cmap_name)
        self.norm = mcolors.BoundaryNorm
        # Initialize the references to the figure elements
        self.imshow = None  # We will visualize 2d scalar fields with imshow
        self.colorbar = None
        self.contour = None  # We may also visualize as contours


class VectorFieldProperties(BaseFieldProperties):
    """
    Class to manage the properties of vector fields we need for visualization.
    """

    def __init__(
        self, name, fields: None | dict[str, NDArray[np.complex128]], quiver_scale=2.5
    ):
        self.name = name
        self.fields = fields
        self.quiver = None
        self.quiver_key = None
        self.quiver_scale = quiver_scale
        self.quiver_width = 0.006


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
        figsize: tuple[float] = (5, 4),
        field_properties: None | dict[str, BaseFieldProperties] = None,
    ):
        """Initialize the model."""
        self.name = name
        self.fig: plt.Figure
        self.ax: plt.Axes
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.cache = WebCache()
        self.x = x
        self.z = z
        self.X: NDArray[np.complex128]
        self.Z: NDArray[np.complex128]
        self.X, self.Z = np.meshgrid(x, z)
        self.field_properties = field_properties
        self._current_imshow_field: str | None = None
        self._current_contour_field: str | None = None
        self._current_quiver_field: str | None = None


def is_dimensional_mode():
    """Check if dimensional mode is active."""
    dim_radio = document.getElementById("dimensional-button")
    return dim_radio.checked if dim_radio else False
