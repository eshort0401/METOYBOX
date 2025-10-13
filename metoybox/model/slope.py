"""Extensions of the BaseWaveModel to flows over sloping topography."""

from metoybox.model import core
from metoybox.calculate import mountain_valley, point_forcing_slope
import matplotlib.colors as mcolors
import numpy as np


class BaseSlopedModel(core.BaseWaveModel):
    """
    A linear theory model for the mountain-valley breeze or low-level jet type flows.
    """

    def __init__(self, *args, **kwargs):
        """See the base class for input documentation."""
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

    def update_displacement_lines(self):
        """Update the displacement lines for sloped models."""
        super().update_displacement_lines()
        # Mask out any displacement lines below the slope
        for line in self.displacement_lines.lines:
            x_data, y_data = line.get_xdata(), line.get_ydata()
            M = self.non_dimensional_variables["M"]
            cond = y_data < M * x_data
            x_data[cond] = np.nan
            y_data[cond] = np.nan
            line.set_xdata(x_data)
            line.set_ydata(y_data)


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


class PointForcingModel(BaseSlopedModel):
    """
    A linear theory model for point forcing over a slope.
    """

    def calculate_fields(self, names):
        """Calculate the fields for the point forcing over slope model."""
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
