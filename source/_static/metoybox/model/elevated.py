"""Extensions of the BaseWaveModel elevated forcings."""

from metoybox.model import core
from metoybox.calculate import localized_line_forcing


class LocalizedLineForcingModel(core.BaseWaveModel):
    """
    A linear theory model for an elevated localized line forcing.
    """

    def calculate_fields(self, names):
        """Calculate the fields for the elevated localized line forcing model."""

        # Update imshow field
        new_fields = localized_line_forcing.calculate_fields_spatial(
            self.X,
            self.Z,
            self.non_dimensional_variables["L"],
            self.non_dimensional_variables["z_f"],
            self.non_dimensional_variables["f_omega"],
            self.non_dimensional_variables["alpha_omega"],
            self.non_dimensional_variables["N_omega"],
            fields=names,
        )
        return new_fields
