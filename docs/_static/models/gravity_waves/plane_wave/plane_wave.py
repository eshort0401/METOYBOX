import numpy as np
from metoybox.model import foundation
from metoybox.model import core
from metoybox.pyscript_controllers import core as ctl_core
from metoybox.pyscript_controllers.utils import initialize_from_controllers
from js import document


# Configure the model
x = np.linspace(-2, 2, 201)
z = np.linspace(0, 4, 201)

x_ticks = np.arange(-2, 3, 1)
z_ticks = np.arange(0, 5, 1)
x_limits = (-2, 2)
z_limits = (0, 4)
u = core.Velocity(percentile=95).fields["u"]
w = core.Velocity(percentile=95).fields["w"]
fields = {"psi": core.Psi(percentile=95), "u": u, "w": w}
fields.update({"velocity": core.Velocity(percentile=95)})
fields.update({"grad_phi": core.GradPhi(percentile=95)})
fields.update({"v": core.V(percentile=95), "phi": core.Phi(percentile=95)})
fields.update({"xi": core.Xi(), "zeta": core.Zeta()})

# Create a field for the b scalar fields and bk vector field
cm_formatter = core.UnitFormatter("cm s$^{-2}$", 1e2)
mm_formatter = core.UnitFormatter("mm s$^{-2}$", 1e3)
# m_formatter = core.UnitFormatter("m s$^{-2}$", 1)
# Note b=b_w for the plane wave model
b_w = core.ScalarField("b_w", r"$b$", cm_formatter, max_upper=0.1, percentile=95)
zero_field = core.ScalarField("zero", r"0", cm_formatter, percentile=95)
b = core.VectorField("buoyancy", r"$b\mathbf{k}$", {"zero": zero_field, "b_w": b_w})
# Create a field for the coriolis acceleration f*v in the x-direction
coriolis_x = core.ScalarField(
    "coriolis_x", r"$fv$", cm_formatter, max_upper=0.1, percentile=95
)
# Might need to implement different labels for different coordinate systems?
coriolis = core.VectorField(
    "coriolis",
    r"$fv\mathbf{i}$",
    {"coriolis_x": coriolis_x, "zero": zero_field},
    non_dim_label=r"$\frac{f}{\omega}v\mathbf{i}$",
    percentile=95,
)

a_x = core.ScalarField("a_x", r"$a_x$", cm_formatter, max_upper=0.1, percentile=95)
a_z = core.ScalarField("a_z", r"$a_z$", cm_formatter, max_upper=0.1, percentile=95)
acceleration = core.VectorField(
    "acceleration",
    r"$\mathbf{a}$",
    {"a_x": a_x, "a_z": a_z},
    percentile=95,
)

fields.update({"buoyancy": b, "coriolis": coriolis, "acceleration": acceleration})

args = ["plane_wave", x, z, x_ticks, z_ticks, x_limits, z_limits]
model = foundation.PlaneWaveModel(*args, fields=fields)

dim_var = ctl_core.default_dimensional.copy() + ["sigma_dim", "k_dim"]
# We don't need Q_0 for the plane wave model
dim_var.remove("Q_0")
non_dim_var = ctl_core.default_non_dimensional.copy() + ["sigma", "k"]

# Enforce consistency between initial slider values and initial model values
initialize_from_controllers(model)

script = document.currentScript
container_id = script.getAttribute("data-container-id")
controller = ctl_core.BaseWaveController(model, container_id, dim_var, non_dim_var)
ctl_core.hide_loading_screen(container_id)
