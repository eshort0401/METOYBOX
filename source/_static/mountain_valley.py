import numpy as np
import sys
from pathlib import Path


from metoybox.model import slope
from metoybox.model import core
from metoybox.pyscript_controllers import core as ctl_core


# Configure the model
x = np.linspace(-2, 2, 201)
z = np.linspace(-1, 4, 401)
x_ticks = np.arange(-2, 3, 1)
z_ticks = np.arange(-1, 4, 1)
x_limits = (-2, 2)
z_limits = (-1, 3)
fields = {"psi": core.Psi(), "Q": core.Q(), "velocity": core.Velocity()}
fields.update({"v": core.V(), "phi": core.Phi(), "xi": core.Xi(), "zeta": core.Zeta()})
args = ["mountain_valley", x, z, x_ticks, z_ticks, x_limits, z_limits]
model = slope.MountainValleyModel(*args, fields=fields)

dim_var = ctl_core.default_dimensional.copy() + ["M_dim"]
non_dim_var = ctl_core.default_non_dimensional.copy() + ["M"]
controller = ctl_core.BaseWaveController(model, dim_var, non_dim_var)
ctl_core.hide_loading_screen()
