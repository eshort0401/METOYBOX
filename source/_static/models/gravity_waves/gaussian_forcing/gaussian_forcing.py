import numpy as np
from pathlib import Path
from pathlib import Path
from metoybox.model import elevated
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
fields.update({"v": core.V(percentile=95), "phi": core.Phi(percentile=95)})
fields.update({"xi": core.Xi(), "zeta": core.Zeta()})
args = ["point_forcing", x, z, x_ticks, z_ticks, x_limits, z_limits]
model = elevated.GaussianTemporalForcingModel(*args, fields=fields)

dim_var = ctl_core.default_dimensional.copy() + ["z_f_dim", "omega", "sigma_dim"]
non_dim_var = ctl_core.default_non_dimensional.copy() + ["z_f", "sigma"]


# Enforce consistency between initial slider values and initial model values
initialize_from_controllers(model)

script = document.currentScript
container_id = script.getAttribute('data-container-id')
controller = ctl_core.BaseWaveController(model, container_id, dim_var, non_dim_var)
ctl_core.hide_loading_screen(container_id)