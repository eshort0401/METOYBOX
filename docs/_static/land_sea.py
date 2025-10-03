import numpy as np


from metoybox.model import land_sea
from metoybox.model import core
from metoybox.pyscript_controllers import core as ctl_core


# Configure the model
x = np.linspace(-3, 4, 201)
z = np.linspace(0, 6, 201)

x_ticks = np.arange(-3, 4, 1.5)
z_ticks = np.arange(0, 7, 1.5)
x_limits = (-3, 3)
z_limits = (0, 6)
fields = {"psi": core.Psi(percentile=90), "velocity": core.Velocity(percentile=90)}
fields.update({"v": core.V(percentile=90), "Q": core.Q()})
fields.update({"xi": core.Xi(), "zeta": core.Zeta()})
args = ["land_sea", x, z, x_ticks, z_ticks, x_limits, z_limits]
model = land_sea.LandSeaBreezeModel(*args, fields=fields)

dim_var = ctl_core.default_dimensional.copy() + ["L_dim"]
non_dim_var = ctl_core.default_non_dimensional.copy() + ["L"]
controller = ctl_core.BaseWaveController(model, dim_var, non_dim_var)
ctl_core.hide_loading_screen()
