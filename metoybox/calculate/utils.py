from typing import List
from numpy.typing import NDArray


def recover_polarized_default(
    u: NDArray,
    w: NDArray,
    f_omega: float,
    alpha_omega: float,
    fields: List[str] = ["v", "xi", "zeta", "phi"],
    sigma: float = 1,
) -> dict:
    """Get the requisite fields from the default polarization relations."""
    fields_dict = {}
    sigma_hat = 1j * sigma + alpha_omega
    fields_dict["b_w"] = -w / sigma_hat

    fields_dict["v"] = -f_omega / sigma_hat * u
    if "xi" in fields:
        fields_dict["xi"] = -1j * u / sigma
    if "zeta" in fields:
        fields_dict["zeta"] = -1j * w / sigma
    
    return fields_dict
