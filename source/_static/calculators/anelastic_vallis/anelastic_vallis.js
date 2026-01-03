// Note containerID is set by utils.py

// Setup constants
const c_p = 1005; // J kg^-1 K^-1
const c_v = 718; // J kg^-1 K^-1
const gamma = c_p / c_v;
const R = c_p - c_v; // J kg^-1 K^-1
const g = 9.81; // m s^-2

// Define reference values
const p_s = 1e5; // Pa
const T_s = 300; // K
const rho_s = p_s / (R * T_s); // Ideal gas law

createSliderRow(
    `${containerID}-u-slider`,
    `${containerID}-u-output`,
    "\\(u:\\)",
    1,
    50,
    10,
    "dimensional",
    "m s⁻1"
);

createSliderRow(
    `${containerID}-w-slider`,
    `${containerID}-w-output`,
    "\\(w:\\)",
    1,
    50,
    10,
    "dimensional",
    "m s⁻1"
);

// Get the relevant div container
const container = document.querySelector(
    `#${containerID} #main-content #controls`
);
// Append all the control rows to the container

container.append(...Object.values(sliders));
