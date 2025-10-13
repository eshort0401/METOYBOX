from typing import List
from numpy.typing import NDArray


def recover_polarized_default(
    u: NDArray,
    w: NDArray,
    f_omega: float,
    alpha_omega: float,
    fields: List[str] = ["v", "xi", "zeta", "phi"],
) -> dict:
    """Get the requisite fields from the default polarization relations."""
    fields_dict = {}
    sigma_hat = 1j + alpha_omega

    if "v" in fields:
        fields_dict["v"] = -f_omega / sigma_hat * u
    if "xi" in fields:
        fields_dict["xi"] = -1j * u
    if "zeta" in fields:
        fields_dict["zeta"] = -1j * w
    if "bw" in fields:
        fields_dict["bw"] = -w / sigma_hat
    return fields_dict
