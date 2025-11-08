import numpy as np


from metoybox.model import land_sea
from metoybox.model import core
from metoybox.pyscript_controllers import core as ctl_core


# Configure the model
x = np.linspace(-2, 2, 201)
z = np.linspace(0, 4, 201)

x_ticks = np.arange(-2, 3, 1)
z_ticks = np.arange(0, 5, 1)
x_limits = (-2, 2)
z_limits = (0, 4)
u = core.Velocity(percentile=95).fields["u"]
w = core.Velocity(percentile=95).fields["w"]
fields = {"psi": core.Psi(percentile=85), "u": u, "w": w}
fields.update({"velocity": core.Velocity(percentile=99)})
fields["velocity"].fields["u"].percentile = 85
fields["velocity"].fields["w"].percentile = 85
fields.update({"v": core.V(percentile=85), "Q": core.Q()})
fields.update({"xi": core.Xi(), "zeta": core.Zeta()})
args = ["land_sea", x, z, x_ticks, z_ticks, x_limits, z_limits]
model = land_sea.LandSeaBreezeModel(*args, fields=fields)
# Use a more interesting startig time
# Note we also must update the starting slider value in land_sea.html
model.non_dimensional_variables["t"] = np.pi / 2

dim_var = ctl_core.default_dimensional.copy() + ["L_dim"]
non_dim_var = ctl_core.default_non_dimensional.copy() + ["L"]
controller = ctl_core.BaseWaveController(model, dim_var, non_dim_var)
ctl_core.hide_loading_screen()
