"""Base classes for building pyscript controllers."""

from metoybox.model.core import BaseWaveModel
from typing import Iterable

from pyscript import document, display, when


class WebCache:
    """Cache for DOM elements to avoid repeated lookups."""

    def __init__(self):
        self.elements = {}

    def get(self, element_id):
        if element_id not in self.elements:
            element = document.getElementById(element_id)
            if element is None:
                print(f"Missing DOM element: '{element_id}'")
                return None
            self.elements[element_id] = element
        return self.elements[element_id]


# Define some default controllable variables. Note these can be a subset of those
# defined for the model, i.e. not all variables need to be controllable. For instance,
# omega will often be fixed.
default_non_dimensional = ["t", "N_omega", "alpha_omega", "f_omega"]
default_dimensional = ["t_dim", "N", "alpha", "f", "Q_0", "H"]


class BaseWaveController:
    """Base class for pyscript controllers."""

    def __init__(
        self,
        model: BaseWaveModel,
        dimensional_variables: Iterable[str] = default_dimensional,
        non_dimensional_variables: Iterable[str] = default_non_dimensional,
        target: str = "figure-output",
    ):
        """
        Initialize the controller. This sets up the web cache and registers all the
        event handlers with pyscript.
        """
        self.cache = WebCache()
        self.target = target
        self.model = model
        self.dimensional_variables = dimensional_variables
        self.non_dimensional_variables = non_dimensional_variables
        self.dimensional_sliders = [f"{name}-slider" for name in dimensional_variables]
        self.non_dimensional_sliders = [
            f"{name}-slider" for name in non_dimensional_variables
        ]
        self._check_variables()
        self._register_event_handlers()
        self.model.initialize_figure()
        self.model.update_fields()
        self.model.update_suptitle()
        self.model.update_figure_data()
        display(self.model.fig, target="figure-output", append=False)

    def _check_variables(self):
        """Check that the model contains the required variables."""
        dim_var = list(self.model.dimensional_variables.keys())
        non_dim_var = list(self.model.non_dimensional_variables.keys())
        if "t" not in non_dim_var:
            raise ValueError("Non-dimensional time variable 't' must be in model.")
        if "t_dim" not in dim_var:
            raise ValueError("Dimensional time variable 't_dim' must be in model.")
        for name in self.dimensional_variables:
            if name not in dim_var:
                message = f"Dimensional controller variable '{name}' not in model."
                raise ValueError(message)
        for name in self.non_dimensional_variables:
            if name not in non_dim_var:
                message = f"Non-dimensional controller variable '{name}' not in model."
                raise ValueError(message)

    def _register_event_handlers(self):
        """Register all event handlers."""

        @when("change", "#dimensional-button, #non-dimensional-button")
        def _change_coordinates(event):
            """Handle coordinate system change."""
            self.change_coordinates(event)

        time_sliders = ["t-slider", "t_dim-slider"]
        model_sliders = self.dimensional_sliders + self.non_dimensional_sliders
        model_sliders = [s for s in model_sliders if s not in time_sliders]
        model_slider_str = "#" + ", #".join(model_sliders)
        time_slider_str = "#" + ", #".join(time_sliders)

        @when("input", model_slider_str)
        def _update_model_variables(event):
            """Update the model variables based on the controller inputs."""
            self.update_model_variables(event)

        @when("input", time_slider_str)
        def _update_time(event):
            """Update the time variable."""
            self.update_time(event)

    def _is_dimensional_mode(self):
        """Check if the controller is in dimensional mode."""
        button = self.cache.get("dimensional-button")
        return button.checked if button else False

    def _update_values(
        self, new_values: dict[str, float], control_suffix: str = "-slider"
    ):
        """Update the controller values (e.g. the sliders.)"""
        for name, value in new_values.items():
            control = self.cache.get(f"{name}{control_suffix}")
            control.value = str(value)

    def _update_outputs(
        self,
        names: Iterable[str],
        control_suffix: str = "-slider",
        output_suffix: str = "-out",
    ):
        """Update the controller outputs (e.g. the text next to a slider.)"""
        for name in names:
            value = float(self.cache.get(f"{name}{control_suffix}").value)
            out = self.cache.get(f"{name}{output_suffix}")
            if out.units:
                out.textContent = f"{value:.1e}" + f" {out.units}"
            else:
                out.textContent = f"{value:.2f}"

    def change_coordinates(self, event):
        """Handle coordinate system change."""
        dim_var = self.model.dimensional_variables
        non_dim_var = self.model.non_dimensional_variables
        if self._is_dimensional_mode():
            self.model.coordinates = "dimensional"
            # Make sure the dimensional variables are consistent with the last values
            # of the non-dimensional variables
            new_var = self.model.match_non_dimensional(dim_var, non_dim_var)
            self.model.dimensional_variables.update(new_var)
            # Now restrict to just those variables that are controlled
            ctl_var = self.dimensional_variables
            new_var = {k: v for k, v in new_var.items() if k in ctl_var}
        else:
            self.model.coordinates = "non-dimensional"
            new_var = self.model.match_dimensional(dim_var, non_dim_var)
            self.model.non_dimensional_variables.update(new_var)
            ctl_var = self.non_dimensional_variables
            new_var = {k: v for k, v in new_var.items() if k in ctl_var}
        # Update the controller values
        self._update_values(new_var)
        # Update the controller value label
        self._update_outputs(new_var.keys())
        self.model.update_scalings()
        self.model.update_labels()
        self.model.update_fields()
        self.model.update_figure_data()
        self.model.update_suptitle()
        display(self.model.fig, target="figure-output", append=False)

    def update_model_variables(self, event, control_suffix: str = "-slider"):
        """Update the model variables based on the controller inputs."""
        name = event.target.id
        key = name.replace(control_suffix, "")
        control = self.cache.get(name)
        if self._is_dimensional_mode():
            self.model.dimensional_variables[key] = float(control.value)
            self.model.update_scalings()
            self.model.update_labels()
        else:
            self.model.non_dimensional_variables[key] = float(control.value)
        self._update_outputs([key])
        self.model.update_fields()
        self.model.update_figure_data()
        display(self.model.fig, target="figure-output", append=False)

    def update_time(self, event):
        """Update the time variable."""
        if self._is_dimensional_mode():
            t_dim = float(self.cache.get("t_dim-slider").value)
            self.model.dimensional_variables["t_dim"] = t_dim
            omega = self.model.dimensional_variables["omega"]
            t = t_dim * omega
            self.model.non_dimensional_variables["t"] = t
            self._update_outputs(["t_dim"])
        else:
            t = float(self.cache.get("t-slider").value)
            self.model.non_dimensional_variables["t"] = t
            self._update_outputs(["t"])
        self.model.update_figure_data()
        self.model.update_suptitle()
        display(self.model.fig, target="figure-output", append=False)


def hide_loading_screen():
    """Hide loading screen and show main content"""
    loading_screen = document.getElementById("loading-screen")
    main_content = document.getElementById("main-content")

    loading_screen.style.display = "none"
    main_content.style.display = "block"
