"""Extensions of the BaseWaveModel elevated forcings."""

from metoybox.model import core
from metoybox.calculate import foundation


class FoundationWaveModel(core.BaseWaveModel):
    """
    A basic plane wave.
    """

    def calculate_fields(self, names):
        """Calculate the fields for the elevated localized line forcing model."""

        # Update imshow field
        new_fields = foundation.calculate_fields_spatial(
            self.X,
            self.Z,
            self.non_dimensional_variables["k"],
            self.non_dimensional_variables["sigma"],
            self.non_dimensional_variables["f_omega"],
            self.non_dimensional_variables["alpha_omega"],
            self.non_dimensional_variables["N_omega"],
            fields=names,
        )
        return new_fields