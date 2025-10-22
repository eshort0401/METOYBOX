import numpy as np


from metoybox.model import slope
from metoybox.model import core
from metoybox.pyscript_controllers import core as ctl_core


# Configure the model
x = np.linspace(-2.25, 2.25, 201)
z = np.linspace(-1, 4, 301)

x_ticks = np.arange(-2, 3, 1)
z_ticks = np.arange(-1, 4, 1)
x_limits = (-2, 2)
z_limits = (-1, 3)
u = core.Velocity(percentile=90).fields["u"]
w = core.Velocity(percentile=90).fields["w"]
fields = {"psi": core.Psi(percentile=90), "u": u, "w": w}
fields.update({"velocity": core.Velocity(percentile=90)})
fields.update({"v": core.V(percentile=90), "phi": core.Phi(percentile=90)})
fields.update({"xi": core.Xi(), "zeta": core.Zeta()})
args = ["point_forcing", x, z, x_ticks, z_ticks, x_limits, z_limits]
model = slope.PointForcingModel(*args, fields=fields)

dim_var = ctl_core.default_dimensional.copy() + ["M_dim", "z_f_dim", "omega"]
non_dim_var = ctl_core.default_non_dimensional.copy() + ["M", "z_f"]
controller = ctl_core.BaseWaveController(model, dim_var, non_dim_var)
ctl_core.hide_loading_screen()
