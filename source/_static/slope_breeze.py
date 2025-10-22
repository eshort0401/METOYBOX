import numpy as np
from metoybox.model import slope
from metoybox.model import core
from metoybox.pyscript_controllers import core as ctl_core


# Configure the model
x = np.linspace(-2.5, 2.5, 251)
z = np.linspace(-1, 4, 251)
x_ticks = np.arange(-2, 3, 1)
z_ticks = np.arange(-1, 4, 1)
x_limits = (-2, 2)
z_limits = (-1, 3)
u = core.Velocity().fields["u"]
w = core.Velocity().fields["w"]
fields = {"psi": core.Psi(), "u": u, "w": w, "Q": core.Q(), "velocity": core.Velocity()}
fields.update({"v": core.V(), "phi": core.Phi(), "xi": core.Xi(), "zeta": core.Zeta()})
args = ["mountain_valley", x, z, x_ticks, z_ticks, x_limits, z_limits]
# Note max upper scale is for the displacement lines... allow large displacements for
# this model!
model = slope.MountainValleyModel(*args, fields=fields, max_upper_scale=5)

dim_var = ctl_core.default_dimensional.copy() + ["M_dim"]
non_dim_var = ctl_core.default_non_dimensional.copy() + ["M"]
controller = ctl_core.BaseWaveController(model, dim_var, non_dim_var)
ctl_core.hide_loading_screen()
