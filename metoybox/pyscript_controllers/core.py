"""Base classes for building pyscript controllers."""

from typing import Literal
from metoybox.model.core import BaseWaveModel
from typing import Iterable

# Import pyscript. Note these are not normal imports and typically confuse IDE linters!
from pyscript import document, display, when
from pyodide.ffi import create_proxy
from js import window


class WebCache:
    """Cache for DOM elements to avoid repeated lookups."""

    def __init__(self, container):
        self.elements = {}
        self.container = container

    def get(self, element_id):
        if element_id not in self.elements:
            element = self.container.querySelector(f"#{element_id}")
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
        container_id: str,
        dimensional_variables: Iterable[str] | None = None,
        non_dimensional_variables: Iterable[str] | None = None,
    ):
        """
        Initialize the controller. This sets up the web cache and registers all the
        event handlers with pyscript.
        """
        self.container_id = container_id  # Store the HTML id of the model container div
        self.container = document.getElementById(container_id)
        self.cache = WebCache(self.container)
        self.active_target = f"{container_id}-figure-output-A"
        self.inactive_target = f"{container_id}-figure-output-B"
        self.model = model
        if dimensional_variables is None:
            dimensional_variables = default_dimensional.copy()
        if non_dimensional_variables is None:
            non_dimensional_variables = default_non_dimensional.copy()
        self.dimensional_variables = dimensional_variables
        self.non_dimensional_variables = non_dimensional_variables
        self.dimensional_sliders = [
            f"{container_id}-{name}-slider" for name in dimensional_variables
        ]
        self.non_dimensional_sliders = [
            f"{container_id}-{name}-slider" for name in non_dimensional_variables
        ]
        self._check_variables()
        self._register_event_handlers()
        name = self._get_active_imshow_field()
        self.model.active_imshow_field = name
        self.model.initialize_figure()
        self.initialize_feature_visibility()
        self.initialize_coordinates()
        self.model.update_fields()
        self.model.update_suptitle()
        self.model.update_labels()
        self.model.update_figure_data()
        display(
            self.model.fig, target=f"{self.container_id}-figure-output-A", append=False
        )
        self.change_coordinates(None)

    def initialize_feature_visibility(self):
        """Initialize the visibility of features based on checkbox/button states."""
        quiver_checkbox = self.cache.get(f"{self.container_id}-quiver-checkbox")
        imshow_checkbox = self.cache.get(f"{self.container_id}-imshow-checkbox")
        displacement_checkbox = self.cache.get(
            f"{self.container_id}-displacement-checkbox"
        )

        self.model.quiver.set_visible(quiver_checkbox.checked)
        if not quiver_checkbox.checked:
            try:
                self.model.quiver_key.remove()
            except ValueError:
                pass
        self.model.quiver_visible = quiver_checkbox.checked

        self.model.imshow.set_visible(imshow_checkbox.checked)
        self.model.colorbar.ax.set_visible(imshow_checkbox.checked)
        self.model.imshow_visible = imshow_checkbox.checked

        self.model.displacement_lines.visible = displacement_checkbox.checked
        self.model.displacement_lines.set_visibility()

    def initialize_coordinates(self):
        """Initialize the coordinate system based on button states."""
        if self._is_dimensional_mode():
            self.model.coordinates = "dimensional"
        else:
            self.model.coordinates = "non-dimensional"

    def redraw(self):
        """Swap active target and redraw the figure."""
        active = self.active_target
        inactive = self.inactive_target
        display(self.model.fig, target=inactive, append=False)

        active_element = self.cache.get(active)
        inactive_element = self.cache.get(inactive)

        def is_ready(element) -> bool:
            """Check if the content in the element is ready to be displayed."""
            child_element = element.firstElementChild or element.lastElementChild
            if not child_element:
                return False
            tag = (child_element.tagName or "").lower()
            if tag == "img":
                # Image decoded and sized
                complete = bool(getattr(child_element, "complete", False))
                width = int(getattr(child_element, "naturalWidth", 0) or 0)
                height = int(getattr(child_element, "naturalHeight", 0) or 0)
                return complete and width > 0 and height > 0
            # SVG/others: ensure it laid out and has size/content
            rect = child_element.getBoundingClientRect()
            check_size = rect.width > 0 and rect.height > 0
            check_child_nodes = child_element.childNodes.length > 0
            return check_size and check_child_nodes

        def poll(timestamp: float):
            if is_ready(inactive_element):
                # Flip visibility (no fade), then swap IDs
                inactive_element.classList.remove("is-passive")
                inactive_element.classList.add("is-active")
                active_element.classList.remove("is-active")
                active_element.classList.add("is-passive")
                self.active_target, self.inactive_target = inactive, active
            else:
                window.requestAnimationFrame(create_proxy(poll))

        window.requestAnimationFrame(create_proxy(poll))

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

        dimensional_str = "#" + f"{self.container_id}-dimensional-button"
        non_dimensional_str = "#" + f"{self.container_id}-non-dimensional-button"
        coords_str = f"{dimensional_str}, {non_dimensional_str}"

        @when("change", coords_str)
        def _change_coordinates(event):
            """Handle coordinate system change."""
            self.change_coordinates(event)

        checkbox_str = f"#{self.container_id}-displacement-checkbox"

        @when("change", checkbox_str)
        def _toggle_displacement_lines(event):
            """Handle displacement lines visibility change."""
            self.toggle_displacement_lines(event)

        quiver_str = f"#{self.container_id}-quiver-checkbox"
        imshow_str = f"#{self.container_id}-imshow-checkbox"
        toggle_str = f"{quiver_str}, {imshow_str}"

        @when("change", toggle_str)
        def _toggle_feature(event):
            """Handle feature visibility change."""
            # Note ID strings have the format {container_id}-{feature}-checkbox
            feature = event.target.id.split("-")[1]
            self.toggle_feature(event, feature)

        time_sliders = [
            f"{self.container_id}-t-slider",
            f"{self.container_id}-t_dim-slider",
        ]
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

        imshow_str = f"input[name='{self.container_id}-imshow-field']"

        @when("change", imshow_str)
        def _change_imshow_field(event):
            """Handle imshow field change."""
            self.change_imshow_field(event)

        quiver_str = f"input[name='{self.container_id}-quiver-field']"

        @when("change", quiver_str)
        def _change_quiver_field(event):
            """Handle quiver field change."""
            self.change_quiver_field(event)

    def _is_dimensional_mode(self):
        """Check if the controller is in dimensional mode."""
        button = self.cache.get(f"{self.container_id}-dimensional-button")
        return button.checked if button else False

    def _get_active_imshow_field(self):
        """Get the currently active imshow field from the relevant buttons."""
        imshow_str = f"{self.container_id}-imshow-field"
        checked = document.querySelector(f"input[name='{imshow_str}']:checked")
        return checked.value if checked else "psi"

    def change_imshow_field(self, event):
        """Handle imshow field change."""
        name = self._get_active_imshow_field()
        self.model.active_imshow_field = name
        self.model.update_fields(force_update_norm=True)
        self.model.update_labels()
        self.model.update_figure_data()
        self.redraw()

    def _get_active_quiver_field(self):
        """Get the currently active quiver field from the relevant buttons."""
        quiver_str = f"{self.container_id}-quiver-field"
        checked = document.querySelector(f"input[name='{quiver_str}']:checked")
        return checked.value if checked else "velocity"

    def change_quiver_field(self, event):
        """Handle quiver field change."""
        name = self._get_active_quiver_field()
        self.model.active_quiver_field = name
        self.model.update_fields(force_update_norm=True)
        self.model.update_labels()
        self.model.update_figure_data()
        self.redraw()

    def toggle_displacement_lines(self, event):
        """Toggle the visibility of the displacement lines."""
        checkbox = event.target
        visible = checkbox.checked
        self.model.displacement_lines.visible = visible
        self.model.displacement_lines.set_visibility()
        if visible:
            self.model.update_fields()
            self.model.update_displacement_lines()
        self.model.update_figure_data()
        self.redraw()

    def toggle_feature(self, event, feature: Literal["quiver", "imshow"]):
        """Toggle the visibility of a feature plot."""
        checkbox = event.target
        visible = checkbox.checked
        feature_handler = getattr(self.model, feature)
        feature_handler.set_visible(visible)
        if feature == "quiver":
            self.model.quiver_visible = visible
            if visible:
                self.model.rebuild_quiver_key()
            else:
                try:
                    self.model.quiver_key.remove()
                except ValueError:
                    pass
        elif feature == "imshow":
            self.model.colorbar.ax.set_visible(visible)
            self.model.imshow_visible = visible
        if visible:
            self.model.update_fields()
        self.model.update_figure_data()
        self.redraw()

    def _update_values(
        self, new_values: dict[str, float], control_suffix: str = "-slider"
    ):
        """Update the controller values (e.g. the sliders.)"""
        for name, value in new_values.items():
            element_id = f"{self.container_id}-{name}{control_suffix}"
            control = self.cache.get(element_id)
            control.value = str(value)

    def _update_outputs(
        self,
        names: Iterable[str],
        control_suffix: str = "-slider",
        output_suffix: str = "-output",
    ):
        """Update the controller outputs (e.g. the text next to a slider.)"""
        for name in names:
            control_id = f"{self.container_id}-{name}{control_suffix}"
            value = float(self.cache.get(control_id).value)
            output_id = f"{self.container_id}-{name}{output_suffix}"
            out = self.cache.get(output_id)
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
        self.redraw()

    def update_model_variables(self, event, control_suffix: str = "-slider"):
        """Update the model variables based on the controller inputs."""
        name = event.target.id
        key = name.replace(control_suffix, "").replace(f"{self.container_id}-", "")
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
        self.redraw()

    def update_time(self, event):
        """Update the time variable."""
        if self._is_dimensional_mode():
            t_dim = float(self.cache.get(f"{self.container_id}-t_dim-slider").value)
            self.model.dimensional_variables["t_dim"] = t_dim
            omega = self.model.dimensional_variables["omega"]
            t = t_dim * omega
            self.model.non_dimensional_variables["t"] = t
            self._update_outputs(["t_dim"])
        else:
            t = float(self.cache.get(f"{self.container_id}-t-slider").value)
            self.model.non_dimensional_variables["t"] = t
            self._update_outputs(["t"])
        self.model.update_figure_data()
        self.model.update_suptitle()
        self.redraw()


def hide_loading_screen(container_id):
    """Hide loading screen and show main content."""

    container = document.getElementById(container_id)
    loading_screen = container.querySelector("#loading-screen")
    main_content = container.querySelector("#main-content")

    loading_screen.style.display = "none"
    main_content.style.display = "block"
