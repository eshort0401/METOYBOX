"""Extensions of the BaseWaveModel to flows over sloping topography."""

from metoybox.model import core
from metoybox.calculate import mountain_valley
import matplotlib.colors as mcolors


# Extend the default model variables to include the slope parameter M
default_dimensional = core.default_dimensional.copy()
default_dimensional.update({"M_dim": core.Omega * 1e2})
default_non_dimensional = core.default_non_dimensional.copy()
default_non_dimensional.update({"M": 0.2})


def get_scalings(
    coordinates: core.CoordinateOptions,
    dimensional_variables: dict[str, float],
    non_dimensional_variables: dict[str, float],
) -> dict[str, float]:
    """
    Get the dictionary of scalings to recover the dimensional variables from the
    non-dimensional variables. Multiply for non-dimensional to dimensional; divide for
    dimensional to non-dimensional.
    """
    dim_var = dimensional_variables
    non_dim_var = non_dimensional_variables
    scalings = core.get_default_scalings(coordinates, dim_var, non_dim_var)
    # Add the slope scaling
    scalings["M"] = dim_var["omega"] / dim_var["N"]
    return scalings


def match_non_dimensional(
    dimensional_variables: dict[str, float],
    non_dimensional_variables: dict[str, float],
) -> dict[str, float]:
    """
    Ensure the variables of the dimensional coordinate system are consistent with the
    non-dimensional coordinate system. Typically this will be called when we change
    coordinates.
    """
    dim_var = dimensional_variables
    non_dim_var = non_dimensional_variables
    matched_dim_var = core.default_match_non_dimensional(dim_var, non_dim_var)
    # Add the slope matching
    matched_dim_var["M_dim"] = non_dim_var["M"] * dim_var["omega"] / dim_var["N"]
    return matched_dim_var


def match_dimensional(
    dimensional_variables: dict[str, float],
    non_dimensional_variables: dict[str, float],
) -> dict[str, float]:
    """
    Ensure the variables of the non-dimensional coordinate system are consistent with
    the dimensional coordinate system. Typically this will be called when we change
    variables.
    """
    dim_var = dimensional_variables
    non_dim_var = non_dimensional_variables
    matched_non_dim_var = core.default_match_dimensional(dim_var, non_dim_var)
    # Add the slope matching
    matched_non_dim_var["M"] = dim_var["M_dim"] * dim_var["N"] / dim_var["omega"]
    return matched_non_dim_var


class BaseSlopedModel(core.BaseWaveModel):
    """
    A linear theory model for the mountain-valley breeze or low-level jet type flows.
    """

    def __init__(self, *args, **kwargs):
        """See the base class for input documentation."""
        kwargs.setdefault("get_scalings", get_scalings)
        kwargs.setdefault("match_non_dimensional", match_non_dimensional)
        kwargs.setdefault("match_dimensional", match_dimensional)
        kwargs.setdefault("dimensional_variables", default_dimensional)
        kwargs.setdefault("non_dimensional_variables", default_non_dimensional)
        super().__init__(*args, **kwargs)
        self.plot = None  # This will store the plot line for the slope.

    def initialize_figure(self, *args, **kwargs):
        """
        See the base class for input documentation.
        """
        super().initialize_figure(*args, **kwargs)

        # Initialize the slope line
        dark_brown = tuple([c * 0.5 for c in mcolors.to_rgb("tab:brown")])
        M = self.non_dimensional_variables["M"]
        kwargs = {"linewidth": 2, "color": dark_brown, "zorder": 1, "rasterized": True}
        self.plot = self.ax.plot(self.x, self.x * M, **kwargs)[0]
        # Set the ax face color to brown so it looks like ground when the imshow is nan
        self.ax.set_facecolor("tab:brown")
        self.active_imshow_field = "psi"
        self.active_quiver_field = "velocity"

    def update_figure_data(self):
        """Update the extra slope line element for sloped models."""
        super().update_figure_data()
        self.plot.set_ydata(self.x * self.non_dimensional_variables["M"])


class MountainValleyModel(BaseSlopedModel):
    """
    A linear theory model for the mountain-valley breeze or low-level jet type flows.
    """

    def calculate_fields(self, names):
        """Calculate the fields for the mountain-valley model."""

        # Update imshow field
        new_fields = mountain_valley.calculate_fields_spatial(
            self.X,
            self.Z,
            self.non_dimensional_variables["M"],
            self.non_dimensional_variables["f_omega"],
            self.non_dimensional_variables["alpha_omega"],
            self.non_dimensional_variables["N_omega"],
            fields=names,
        )
        return new_fields


# Extend the default model variables to include the slope parameter M
point_dimensional = default_dimensional.copy()
point_dimensional.update({"z_f_dim": 1e3})
point_non_dimensional = default_non_dimensional.copy()
point_non_dimensional.update({"z_f": 1.0})


def get_point_scalings(
    coordinates: core.CoordinateOptions,
    dimensional_variables: dict[str, float],
    non_dimensional_variables: dict[str, float],
) -> dict[str, float]:
    """
    Get the dictionary of scalings to recover the dimensional variables from the
    non-dimensional variables. Multiply for non-dimensional to dimensional; divide for
    dimensional to non-dimensional.
    """
    dim_var = dimensional_variables
    non_dim_var = non_dimensional_variables
    scalings = get_scalings(coordinates, dim_var, non_dim_var)
    # Add the slope scaling
    scalings["z_f"] = scalings["z"]
    return scalings


def point_match_non_dim(dim_var, non_dim_var):
    """Amend for the point-forcing model."""
    matched_dim_var = match_non_dimensional(dim_var, non_dim_var)
    matched_dim_var["z_f_dim"] = non_dim_var["z_f"] * dim_var["H"]
    return matched_dim_var


def point_match_dim(dim_var, non_dim_var):
    """Amend for the point-forcing model."""
    matched_non_dim_var = match_dimensional(dim_var, non_dim_var)
    # Add the slope matching
    matched_non_dim_var["z_f"] = dim_var["z_f_dim"] / dim_var["H"]
    return matched_non_dim_var


class PointForcingModel(BaseSlopedModel):
    """
    A linear theory model for point forcing over a slope.
    """

    def __init__(self, *args, **kwargs):
        """See the base class for input documentation."""
        kwargs.setdefault("dimensional_variables", point_dimensional)
        kwargs.setdefault("non_dimensional_variables", point_non_dimensional)
        kwargs.setdefault("get_scalings", get_point_scalings)
        kwargs.setdefault("match_non_dimensional", point_match_non_dim)
        kwargs.setdefault("match_dimensional", point_match_dim)

        super().__init__(*args, **kwargs)
        # Add the point forcing parameter to the dimensional and non-dimensional variables

    def calculate_fields(self, names):
        """Calculate the fields for the point forcing over slope model."""
        from metoybox.calculate import point_forcing_slope

        # Update imshow field
        new_fields = point_forcing_slope.calculate_fields_spatial(
            self.X,
            self.Z,
            self.non_dimensional_variables["M"],
            self.non_dimensional_variables["z_f"],
            self.non_dimensional_variables["f_omega"],
            self.non_dimensional_variables["alpha_omega"],
            self.non_dimensional_variables["N_omega"],
            fields=names,
        )
        return new_fields
