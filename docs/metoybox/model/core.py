"""
Classes for creating and managing interactive figures. Our goal is browser deployment,
but lets try to write these classes in a deployment agnostic way. We will then build
separate pyscript and native plt implementations.
"""

import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from typing import Literal, Callable
from dataclasses import dataclass
import warnings

CoordinateOptions = Literal["dimensional", "non-dimensional"]


def get_default_scalings(
    coordinates: CoordinateOptions,
    dimensional_variables: dict[str, float],
    non_dimensional_variables: dict[str, float],
) -> dict[str, float]:
    """
    Get the dictionary of scalings to recover the dimensional variables from the
    non-dimensional variables. Multiply for non-dimensional to dimensional; divide for
    dimensional to non-dimensional.
    """

    if coordinates == "non-dimensional":
        # If we are using non-dimensional coordinates, get N from N_omega * omega
        N_omega = non_dimensional_variables["N_omega"]
        omega = dimensional_variables["omega"]  # Assume omega is constant
        N = N_omega * omega
    else:
        # If using dimensional coordinates, simply get N from dimensional variables
        N = dimensional_variables["N"]
        omega = dimensional_variables["omega"]  # Assume omega is constant
    # Get the other dimensional parameters
    H, Q_0 = dimensional_variables["H"], dimensional_variables["Q_0"]

    x_scale = (N / omega) * H  # times x to redimensionalize
    y_scale = (N / omega) * H  # times y to redimensionalize
    z_scale = H  # times z to redimensionalize
    psi_scale = Q_0 * H / (N / omega)  # times psi to redimensionalize
    u_scale = Q_0 / (N * omega)  # times u to redimensionalize
    v_scale = Q_0 / (N * omega)  # times v to redimensionalize
    w_scale = Q_0 / (N**2)  # times w to redimensionalize
    Q_scale = Q_0  # times Q to redimensionalize
    t_scale = 1 / omega  # times t to redimensionalize
    b_scale = Q_0 / omega  # times b to redimensionalize
    phi_scale = Q_0 * H / omega  # times phi to redimensionalize
    scalings = {"x": x_scale, "y": y_scale, "z": z_scale, "psi": psi_scale}
    scalings.update({"u": u_scale, "v": v_scale, "w": w_scale, "Q": Q_scale})
    scalings.update({"t": t_scale, "b": b_scale, "phi": phi_scale})
    return scalings


def default_match_non_dimensional(
    dimensional_variables: dict[str, float],
    non_dimensional_variables: dict[str, float],
) -> dict[str, float]:
    """
    Ensure the variables of the dimensional coordinate system are consistent with the
    non-dimensional coordinate system. Typically this will be called when we change
    coordinates.
    """
    omega = dimensional_variables["omega"]  # omega is usually constant
    f = non_dimensional_variables["f_omega"] * omega
    N = non_dimensional_variables["N_omega"] * omega
    alpha = non_dimensional_variables["alpha_omega"] * omega
    t_dim = non_dimensional_variables["t"] / omega
    dimensional_variables.update({"f": f, "N": N, "alpha": alpha, "t_dim": t_dim})

    return dimensional_variables


def default_match_dimensional(
    dimensional_variables: dict[str, float],
    non_dimensional_variables: dict[str, float],
) -> dict[str, float]:
    """
    Ensure the variables of the non-dimensional coordinate system are consistent with
    the dimensional coordinate system. Typically this will be called when we change
    coordinates.
    """
    omega = dimensional_variables["omega"]  # omega is usually constant
    f_omega = dimensional_variables["f"] / omega
    N_omega = dimensional_variables["N"] / omega
    alpha_omega = dimensional_variables["alpha"] / omega
    t = dimensional_variables["t_dim"] * omega
    variables = {"f_omega": f_omega, "N_omega": N_omega}
    variables.update({"alpha_omega": alpha_omega, "t": t})
    non_dimensional_variables.update(variables)

    return non_dimensional_variables


@dataclass
class UnitFormatter:
    """Convenience class for storing unit conversions for figures."""

    figure_unit_label: str = "km"
    figure_unit_scaler: float = 1e-3


class BaseField:
    """
    Base class to manage the properties of fields we need for visualization.
    """

    def __init__(
        self,
        name: str,
        label: str,
        unit_formatter: UnitFormatter,
        field: NDArray[np.complex128],
        # Max upper will determine the maximum level value
        max_upper: float = 1.0,
        # Max lower is the lowest max value before we update the scaling
        # Max upper and max lower are successive half orders of magnitude, e.g.
        # (.1, .5), (.5, 1), (1, 5), (5, 10), (10, 50) etc.
        max_lower: float = 0.5,
        min: float | None = None,
    ):
        """Initialize field properties."""
        self.name = name
        self.label = label
        self.field = field
        self.unit_formatter = unit_formatter
        self.max_upper = max_upper
        self.max_lower = max_lower
        if min is None:
            self.min = -np.abs(max_upper)


class ScalarField(BaseField):
    """
    Class to manage the properties of scalar fields we need for visualization. Typically
    visualization is done with plt.imshow.

    Attributes:
        name (str): Name of the field (e.g., 'psi', 'u', 'w', 'Q').
        max (float): Maximum value for imshow levels.
        cmap_name (str): Colormap name for visualization.
    """

    def __init__(
        self,
        name: str,
        label: str,
        unit_formatter: UnitFormatter,
        field: NDArray[np.complex128] | None = None,
        max_upper: float = 1.0,
        max_lower: float = 0.5,
        min: float | None = None,
        cmap_name: str = "RdBu_r",
    ):
        """Initialize field properties."""
        super().__init__(name, label, unit_formatter, field, max_upper, max_lower, min)
        self.cmap = plt.get_cmap(cmap_name)
        self.levels = np.linspace(self.min, self.max_upper, 21)
        # Store the tick labels in non-dimensional coordinates
        self.colorbar_tick_labels = np.linspace(self.min, self.max_upper, 11)
        _kwargs = {"ncolors": self.cmap.N, "extend": "both"}
        self.norm = mcolors.BoundaryNorm(self.levels, **_kwargs)


class VectorField(BaseField):
    """
    Class to manage the properties of vector fields we need for visualization.
    """

    def __init__(
        self,
        name: str,
        label: str,
        fields: dict[str, ScalarField],  # Typically the x, z components
        quiver_scale: float = 2.5,
        max_upper: float = 0.1,
        max_lower: float = 0.05,
        quiver_key_magnitude: float = 0.5,
    ):
        self.name = name
        self.label = label
        self.fields = fields
        self.quiver_scale = quiver_scale
        self.quiver_key_magnitude = quiver_key_magnitude
        # For vector fields, max and min refer to the magnitude of the vector
        self.max_upper = max_upper
        self.max_lower = max_lower


class Psi(ScalarField):
    """Convenience class for creating psi fields."""

    def __init__(self):
        """Initialize a psi field."""
        formatter = UnitFormatter("m$^2$ s$^{-1}$", 1.0)
        args = ["psi", r"$\psi$", formatter]
        super().__init__(*args, max_upper=0.5)


class U(ScalarField):
    """Convenience class for creating u fields."""

    def __init__(self):
        """Initialize a u field."""
        formatter = UnitFormatter("m s$^{-1}$", 1.0)
        args = ["u", r"$u$", formatter]
        super().__init__(*args, max_upper=1.0)


class W(ScalarField):
    """Convenience class for creating w fields."""

    def __init__(self):
        """Initialize a w field."""
        formatter = UnitFormatter("cm s$^{-1}$", 1e2)
        args = ["w", r"$w$", formatter]
        super().__init__(*args, max_upper=0.2)


class Velocity(VectorField):
    """Convenience class for creating velocity fields."""

    def __init__(self):
        """Initialize a velocity field."""
        u = U()
        w = W()
        fields = {"u": u, "w": w}
        args = ["velocity", r"$\mathbf{v}$", fields]
        super().__init__(*args, quiver_key_magnitude=0.5)


GetScalingsFunction = Callable[
    [CoordinateOptions, dict[str, float], dict[str, float]], dict[str, float]
]
MatchVariablesFunction = Callable[
    [CoordinateOptions, dict[str, float], dict[str, float]],
    dict[str, float],
]

Omega = 2 * np.pi / (24 * 3600)  # Earth's rotation rate in rad/s
default_dimensional = {"t_dim": 0.0, "N": 1e-2, "H": 1e3, "omega": Omega}
default_dimensional.update({"Q_0": 1.2e-5, "alpha": 0.2 * Omega, "f": 0.5 * Omega})
default_non_dimensional = {"t": 0.0, "N_omega": 1e-2 / Omega}
default_non_dimensional.update({"alpha_omega": 0.2, "f_omega": 0.5})


class BaseWaveModel:
    """
    Class for managing the visualization of wave models. Note only the spatial part of
    each field is saved, with the overall field then np.real(Field * exp(i*t)).
    """

    def __init__(
        self,
        name: str,
        x: NDArray[np.complex128],  # In non-dimensional units
        z: NDArray[np.complex128],
        x_ticks: NDArray[np.float64] | None,  # In non-dimensional units
        z_ticks: NDArray[np.float64] | None,
        x_limits: tuple[float, float] | None,  # In non-dimensional units
        z_limits: tuple[float, float] | None,
        active_imshow_field: str = "psi",
        active_quiver_field: str = "velocity",
        dimensional_variables: dict[str, float] = default_dimensional,
        non_dimensional_variables: dict[str, float] = default_non_dimensional,
        x_unit_formatter: UnitFormatter = UnitFormatter("km", 1e-3),
        z_unit_formatter: UnitFormatter = UnitFormatter("km", 1e-3),
        figure_size: tuple[float] = (5.5, 4),
        suptitle_height: float = 1.0,
        fields: dict[str, BaseField] | None = None,
        get_scalings: GetScalingsFunction = get_default_scalings,
        match_dimensional: MatchVariablesFunction = default_match_dimensional,
        match_non_dimensional: MatchVariablesFunction = default_match_non_dimensional,
        scalings: dict[str, float] = {},
    ):
        """Initialize the model."""
        self.name = name
        self.fig: plt.Figure = None
        self.ax: plt.Axes = None
        self.figure_size = figure_size
        self.suptitle_height = suptitle_height
        self.dimensional_variables = dimensional_variables
        self.non_dimensional_variables = non_dimensional_variables
        self.x, self.z, self.x_ticks, self.z_ticks = x, z, x_ticks, z_ticks
        self.x_tick_labels, self.z_tick_labels = None, None
        self.x_limits, self.z_limits = x_limits, z_limits
        self.x_unit_formatter = x_unit_formatter
        self.z_unit_formatter = z_unit_formatter
        self.X: NDArray[np.complex128] = None
        self.Z: NDArray[np.complex128] = None
        self.X, self.Z = np.meshgrid(x, z)
        self.fields = fields
        self.active_imshow_field = active_imshow_field
        self.active_contour_field = None
        self.active_quiver_field = active_quiver_field
        self.imshow, self.quiver, self.contour = None, None, None
        self.quiver_key, self.colorbar_ax, self.colorbar = None, None, None
        # Choose quiver steps so we get approx 10 arrows in each direction
        self.quiver_step_x = len(x) // 10
        self.quiver_step_z = len(z) // 10
        x_slice = slice(int(self.quiver_step_x / 2), None, self.quiver_step_x)
        z_slice = slice(int(self.quiver_step_z / 2), None, self.quiver_step_z)
        self.quiver_subset = (z_slice, x_slice)
        self.quiver_width_x = x[self.quiver_step_x] - x[0]
        self.quiver_width_z = z[self.quiver_step_z] - z[0]
        # Always start in non-dimensional coordinates
        self.coordinates: Literal["dimensional", "non-dimensional"] = "non-dimensional"
        self.get_scalings = get_scalings
        self.scalings = scalings
        self.match_dimensional = match_dimensional
        self.match_non_dimensional = match_non_dimensional
        coord = self.coordinates
        dim, non_dim = self.dimensional_variables, self.non_dimensional_variables
        self.scalings = self.get_scalings(coord, dim, non_dim)

    def initialize_figure(self):
        """Initialize the figure with the fields."""

        # Initialize the figure, axes and layout
        self.fig, self.ax = plt.subplots(1, 1, figsize=self.figure_size)
        self.fig.patch.set_facecolor("#E6E6E6")
        self.X, self.Z = np.meshgrid(self.x, self.z)
        self.ax.set_ylim(self.z_limits)
        self.ax.set_xlim(self.x_limits)
        if self.x_ticks is None:
            self.x_ticks = np.arange(self.x_limits[0], self.x_limits[1] + 1, 1)
        if self.z_ticks is None:
            self.z_ticks = np.arange(self.z_limits[0], self.z_limits[1] + 1, 1)
        self.ax.set_xticks(self.x_ticks)
        self.ax.set_yticks(self.z_ticks)
        # Store a copy of the non-dimensional tick labels
        self.x_tick_labels = [f"{val:.1f}" for val in self.x_ticks]
        self.z_tick_labels = [f"{val:.1f}" for val in self.z_ticks]
        self.ax.set_xticklabels(self.x_tick_labels)
        self.ax.set_yticklabels(self.z_tick_labels)
        self.ax.set_xlabel(r"$x$ [-]")
        self.ax.set_ylabel(r"$z$ [-]")

        # Initialize the imshow
        field = self.fields[self.active_imshow_field]
        kwargs = {"cmap": field.cmap, "norm": field.norm}
        kwargs.update({"origin": "lower", "aspect": "auto", "zorder": 0})
        extent = [self.x.min(), self.x.max(), self.z.min(), self.z.max()]
        kwargs.update({"extent": extent, "norm": field.norm})
        kwargs.update({"rasterized": True})
        dummy_data = np.ones_like(self.Z) * np.nan
        self.imshow = self.ax.imshow(dummy_data, **kwargs)
        divider = make_axes_locatable(self.ax)
        self.colorbar_ax = divider.append_axes("right", size="5.5%", pad=0.25)
        kwargs = {"cax": self.colorbar_ax, "extend": "both"}
        self.colorbar = self.fig.colorbar(self.imshow, **kwargs)
        self.colorbar.set_label(field.label + " [-]")
        cbar_ticks = np.linspace(field.min, field.max_upper, 11)
        self.colorbar.set_ticks(cbar_ticks)
        cbar_ticklabels = [f"{val:.2f}" for val in cbar_ticks]
        self.colorbar.set_ticklabels(cbar_ticklabels)

        # Initialize the quiver
        field = self.fields[self.active_quiver_field]
        quiver_scale = field.quiver_scale
        subset = self.quiver_subset
        args = [self.X[subset], self.Z[subset]]
        args += [dummy_data[subset], dummy_data[subset]]
        kwargs = {"color": "k", "scale": quiver_scale, "width": 0.006}
        kwargs.update({"angles": "xy", "zorder": 2, "rasterized": True})
        self.quiver = self.ax.quiver(*args, **kwargs)
        quiver_key_mag = field.quiver_key_magnitude
        args = [self.quiver, 0.09, 1.05, quiver_key_mag, f"{quiver_key_mag} [-]"]
        kwargs = {"labelpos": "E", "coordinates": "axes"}
        self.quiver_key = self.ax.quiverkey(*args, **kwargs)

        # Initialize the contour
        # Not yet implemented

        # Initialize the displacements
        # Not yet implemented

        self.fig.suptitle("placeholder", y=self.suptitle_height)
        self.fig.tight_layout()
        self.ax.set_aspect("equal")

    def update_scalings(self):
        """Update the scalings dictionary."""
        dim_var = self.dimensional_variables
        non_dim_var = self.non_dimensional_variables
        self.scalings = self.get_scalings(self.coordinates, dim_var, non_dim_var)

    def update_dimensional_variables(self, new_variables):
        """Update the dimensional variables."""
        # Could add a key check here, but probably better to implement on the input side
        # to avoid repeating the check every time we update the variables.
        self.dimensional_variables.update(new_variables)

    def update_non_dimensional_variables(self, new_variables):
        """Update the non-dimensional variables."""
        # Could add a key check here, but probably better to implement on the input side
        # to avoid repeating the check every time we update the variables.
        self.non_dimensional_variables.update(new_variables)

    def match_variables(self):
        """Ensure the variables of both coordinate systems are consistent."""
        dim_var = self.dimensional_variables
        non_dim_var = self.non_dimensional_variables
        if self.coordinates == "dimensional":
            new_var = self.match_dimensional(dim_var, non_dim_var)
            self.non_dimensional_variables = new_var
        else:
            new_var = self.match_non_dimensional(dim_var, non_dim_var)
            self.dimensional_variables = new_var

    def update_suptitle(self, hour_offset=12):
        """Update the figure suptitle."""
        if self.coordinates == "dimensional":
            t_dim = self.dimensional_variables["t_dim"]
            hour = int(np.floor(t_dim / 3600))
            # Note typically t=0 corresponds to 12:00 LST
            hour_LST = int((hour + hour_offset) % 24)
            minute = int(np.floor((t_dim - hour * 3600) / 60))
            second = int(np.round(t_dim - hour * 3600 - minute * 60))
            time_str = f"{hour_LST:02d}:{minute:02d}:{second:02d}"
            self.fig.suptitle(rf"{time_str} [LST]", y=self.suptitle_height)
        else:
            t = self.non_dimensional_variables["t"]
            self.fig.suptitle(rf"$t={t:.2f}$ [-]", y=self.suptitle_height)

    def update_quiver_key_label(self):
        """Get the quiver key label for the appropriate coordinate system."""
        # Next scale the quiver key labels
        if self.coordinates == "dimensional":
            vector_field = self.fields[self.active_quiver_field]
            quiver_key_mag = vector_field.quiver_key_magnitude
            scalar_fields = vector_field.fields
            field_keys = list(scalar_fields.keys())

            def get_component_label(key, scalar_fields):
                """Get the label for the quiver component."""
                field = scalar_fields[key]
                figure_unit_scaler = field.unit_formatter.figure_unit_scaler
                units = field.unit_formatter.figure_unit_label
                mag_1 = quiver_key_mag * self.scalings[key] * figure_unit_scaler
                label = rf"{field.label}: ${mag_1:0.2f}$ {units}"
                return label

            label_1 = get_component_label(field_keys[0], scalar_fields)
            label_2 = get_component_label(field_keys[1], scalar_fields)
            quiver_key_label = label_1 + ", " + label_2
        else:
            mag = self.fields[self.active_quiver_field].quiver_key_magnitude
            quiver_key_label = rf"{mag:0.2f} [-]"
        self.quiver_key_label = quiver_key_label

    def update_colorbar_labels(self):
        """Update the colorbar labels based on active coordinate system."""

        def format_labels(ticks, exp, field_label, unit_label="-"):
            """Format the the colorbar ticks and labels using exponent."""
            if exp < -1 or exp > 2:
                tick_lab = ticks * 10 ** (-exp)
                axis_label = rf"{field_label} [$10^{{{exp}}}$ {unit_label}]"
            else:
                tick_lab = ticks
                axis_label = rf"{field_label} [{unit_label}]"
            return tick_lab, axis_label

        field = self.fields[self.active_imshow_field]
        if self.coordinates == "dimensional":
            # Next scale the cbar ticks of the active imshow field
            cbar_tick_lab = field.colorbar_tick_labels
            # Redimensionalize
            cbar_tick_lab = cbar_tick_lab * self.scalings[field.name]
            # Scale for plot units
            cbar_tick_lab = cbar_tick_lab * field.unit_formatter.figure_unit_scaler
            # Scale the field max
            field_max_dim = field.max_upper * self.scalings[field.name]
            exp = int(np.floor(np.log10(field_max_dim)))
            unit_label = field.unit_formatter.figure_unit_label
            args = [cbar_tick_lab, exp, field.label, unit_label]
            cbar_tick_lab, cbar_axis_label = format_labels(*args)
        else:
            cbar_tick_lab = field.colorbar_tick_labels
            exp = int(np.floor(np.log10(field.max_upper)))
            args = [cbar_tick_lab, exp, field.label]
            cbar_tick_lab, cbar_axis_label = format_labels(*args)

        cbar_tick_lab = [f"{val:.2f}" for val in cbar_tick_lab]
        self.colorbar.set_ticklabels(cbar_tick_lab)
        self.colorbar.set_label(cbar_axis_label)

    def update_labels(self):
        """
        Amend the plot labels based on active coordinate system and the current values
        of the model parameters. Note we don't recalculate anything when switching
        from non-dimensional to dimensional coordinates, we just rescale the labels!
        """

        if self.coordinates == "dimensional":
            # First scale the x, z tick labels, noting labels are stored as numpy float
            # arrays.
            x_tick_lab, z_tick_lab = self.x_ticks, self.z_ticks
            # To get the dimensional x, z labels, take the non-dimensional tick values,
            # multiply by the redimensionalization scale factor, then the scale factor
            # to get the plot units.
            x_formatter = self.x_unit_formatter
            z_formatter = self.z_unit_formatter
            x_fig_unit_scaler = x_formatter.figure_unit_scaler
            z_fig_unit_scaler = z_formatter.figure_unit_scaler
            x_tick_lab = x_tick_lab * self.scalings["x"] * x_fig_unit_scaler
            z_tick_lab = z_tick_lab * self.scalings["z"] * z_fig_unit_scaler
            x_tick_lab = [f"{val:.1f}" for val in x_tick_lab]
            z_tick_lab = [f"{val:.1f}" for val in z_tick_lab]
            x_axis_lab = rf"$x$ [{x_formatter.figure_unit_label}]"
            z_axis_lab = rf"$z$ [{z_formatter.figure_unit_label}]"

        else:
            x_tick_lab, z_tick_lab = self.x_tick_labels, self.z_tick_labels
            x_axis_lab = r"$x$ [-]"
            z_axis_lab = r"$z$ [-]"

        self.update_quiver_key_label()
        self.quiver_key.text.set_text(self.quiver_key_label)
        self.update_colorbar_labels()
        self.ax.set_xticklabels(x_tick_lab)
        self.ax.set_yticklabels(z_tick_lab)
        self.ax.set_xlabel(x_axis_lab)
        self.ax.set_ylabel(z_axis_lab)

    def update_figure_data(self):
        """Update the figure data based on the current fields and time."""
        if self.coordinates == "dimensional":
            t_dim = self.dimensional_variables["t_dim"]
            t = t_dim / self.scalings["t"]
        else:
            t = self.non_dimensional_variables["t"]

        imshow_field = self.fields[self.active_imshow_field]
        imshow_data = np.real(imshow_field.field * np.exp(1j * t))
        self.imshow.set_data(imshow_data)

        quiver_field = self.fields[self.active_quiver_field]
        component_fields = quiver_field.fields
        keys = list(component_fields.keys())
        field_1 = np.real(component_fields[keys[0]].field * np.exp(1j * t))
        field_2 = np.real(component_fields[keys[1]].field * np.exp(1j * t))
        subset = self.quiver_subset
        self.quiver.set_UVC(field_1[subset], field_2[subset])

        # Update the contour
        # Not yet implemented

    def get_active_fields(self):
        """Return all the active scalars fields. Typically used for updating."""
        names = [self.active_imshow_field]
        vec_field = self.fields[self.active_quiver_field]
        components = list(vec_field.fields.keys())
        names += components
        return names

    def calculate_fields(self, fields):
        """Calculate the model fields in non-dimensional units."""
        # This method should be implemented in subclasses
        message = "calculate_fields is model specific and should be implemented in "
        message += "subclasses."
        raise NotImplementedError(message)

    def update_fields(self):
        """Update the fields and the requisite figure elements."""

        # Update imshow field
        names = self.get_active_fields()
        self.match_variables()
        new_fields = self.calculate_fields(names)
        name = self.active_imshow_field
        self.fields[name].field = new_fields[name]
        current_max = np.nanmax(np.abs(new_fields[name]))
        max_upper = self.fields[name].max_upper
        max_lower = self.fields[name].max_lower
        # Don't rescale if the field is extremely small
        if current_max > 1e-8 and (current_max > max_upper or current_max < max_lower):
            # Reset max_upper and max_lower
            max_lower, max_upper = bounds_half_order_magnitude(current_max)
            self.fields[name].max_lower = max_lower
            self.fields[name].max_upper = max_upper
            self.fields[name].min = -max_upper
            self.fields[name].levels = np.linspace(self.fields[name].min, max_upper, 21)
            tick_labels = np.linspace(self.fields[name].min, max_upper, 11)
            self.fields[name].colorbar_tick_labels = tick_labels
            field = self.fields[name]
            _kwargs = {"ncolors": field.cmap.N, "extend": "both"}
            self.fields[name].norm = mcolors.BoundaryNorm(field.levels, **_kwargs)
            # Update the imshow with new norm
            self.imshow.norm = field.norm
            self.colorbar.update_normal(self.imshow)
            # Update the ticks after change of normal
            self.colorbar.set_ticks(tick_labels)
            self.update_colorbar_labels()

        # Update quiver field
        name = self.active_quiver_field
        quiv_names = list(self.fields[name].fields.keys())
        new_comp_1 = new_fields[quiv_names[0]]
        new_comp_2 = new_fields[quiv_names[1]]
        self.fields[name].fields[quiv_names[0]].field = new_comp_1
        self.fields[name].fields[quiv_names[1]].field = new_comp_2
        magnitude = np.sqrt(np.abs(new_comp_1) ** 2 + np.abs(new_comp_2) ** 2)
        current_max = np.nanmax(magnitude)
        max_upper = self.fields[name].max_upper
        max_lower = self.fields[name].max_lower

        if current_max > max_upper or current_max < max_lower:
            max_lower, max_upper = bounds_half_order_magnitude(current_max)
            self.fields[name].max_lower = max_lower
            self.fields[name].max_upper = max_upper
            self.fields[name].quiver_key_magnitude = max_upper / 2
            max_spacing = np.max([self.quiver_width_x, self.quiver_width_z])
            self.fields[name].quiver_scale = max_upper / max_spacing

            # Redraw the quiver with new scale
            self.quiver.remove()
            quiver_scale = self.fields[name].quiver_scale
            subset = self.quiver_subset
            args = [self.X[subset], self.Z[subset]]
            args += [new_comp_1[subset], new_comp_2[subset]]
            kwargs = {"color": "k", "scale": quiver_scale, "width": 0.006}
            kwargs.update({"angles": "xy", "zorder": 2, "rasterized": True})
            kwargs.update({"scale_units": "xy"})
            self.quiver = self.ax.quiver(*args, **kwargs)

            self.quiver_key.remove()
            quiver_key_mag = self.fields[name].quiver_key_magnitude
            args = [self.quiver, 0.09, 1.05, quiver_key_mag, f"{quiver_key_mag} [-]"]
            kwargs = {"labelpos": "E", "coordinates": "axes"}
            self.quiver_key = self.ax.quiverkey(*args, **kwargs)
            self.update_quiver_key_label()
            self.quiver_key.text.set_text(self.quiver_key_label)


def bounds_half_order_magnitude(value):
    """Round up to nearest half order of magnitude."""
    if value <= 0:
        return 0, 0

    if value <= 0:
        return (0, 0)

    log_val = np.log10(value)
    order = np.floor(log_val)
    mantissa = value / 10**order

    # Find lower and upper bounds
    if mantissa <= 1:
        lower = 0.5
        upper = 1
    elif mantissa <= 5:
        lower = 1
        upper = 5
    else:
        lower = 5
        upper = 10

    lower_bound = lower * 10**order
    upper_bound = upper * 10**order

    return (lower_bound, upper_bound)
