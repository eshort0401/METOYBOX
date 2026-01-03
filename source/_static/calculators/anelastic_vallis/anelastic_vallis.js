// Note containerID is set by utils.py
const table_container = document.querySelector(
    `#${containerID} #main-content #scale-table`
);

const delPSliderRow = createSliderRow(
    `${containerID}-del_p-slider`,
    `${containerID}-del_p-output`,
    "\\(\\delta p:\\)",
    1, // 1 Pa
    10e2, // 10 hPa
    10,
    1,
    "dimensional",
    "Pa"
);

const pBarSliderRow = createSliderRow(
    `${containerID}-p_bar-slider`,
    `${containerID}-p_bar-output`,
    "\\(\\overline{p}:\\)",
    100e2, // 100 hPa
    1000e2, // 1000 hPa
    800e2,
    1,
    "dimensional",
    "Pa"
);

const delRhoSliderRow = createSliderRow(
    `${containerID}-del_rho-slider`,
    `${containerID}-del_rho-output`,
    "\\(\\delta \\rho:\\)",
    1e-3, 
    5e-1,
    10,
    1e-3,
    "dimensional",
    "Pa"
);

const rhoBarSliderRow = createSliderRow(
    `${containerID}-rho_bar-slider`,
    `${containerID}-rho_bar-output`,
    "\\(\\overline{\\rho}:\\)",
    0.1,
    1.25,
    1,
    .01,
    "dimensional",
    "Pa"
);

// Build the scale table
const scaleTable = new ScaleTable(
    [[`${containerID}-a`, `${containerID}-b`, `${containerID}-c`]],
    [[
        "\\frac{1}{\\gamma}\\frac{\\delta p}{\\overline{p}}", 
        "-\\frac{\\delta \\rho}{\\overline{\\rho}}", 
        "R\\left(\\frac{\\delta p}{\\overline{p}}, \\frac{\\delta \\rho}{\\overline{\\rho}}\\right)"]],
    [[10, 10, 10]],
    [["", "", ""]],
);
scaleTable.id = `${containerID}-scale-table`;
// Append the table to the container
table_container.appendChild(scaleTable.table);

// Get the relevant div container
const controls = document.querySelector(
    `#${containerID} #main-content #controls`
);
// Append all the control rows to the container
controls.append(delPSliderRow, pBarSliderRow);

// Setup constants
const c_p = 1005; // J kg^-1 K^-1
const c_v = 718; // J kg^-1 K^-1
const gamma = c_p / c_v;
const R = c_p - c_v; // J kg^-1 K^-1
const g = 9.81; // m s^-2
const Omega = (2 * Math.PI) / (24 * 3600); // rad s^-1

// Define reference values
const p_s = 1e5; // Pa
const T_s = 300; // K
const rho_s = p_s / (R * T_s); // Ideal gas law

function calculateTerms(u, w, t, f, p_bar, rho_bar, del_p, del_rho) {
    const L = u * t;
    const H = w * t;
    const del_phi_exact =
        (1 / gamma) * Math.log((p_bar + del_p) / p_bar) -
        Math.log((rho_bar + del_rho) / rho_bar);
    const del_phi_1 = (1 / gamma) * (del_p / p_bar);
    const del_phi_2 = -(del_rho / rho_bar);
    const del_phi_3 = del_phi_exact - del_phi_1 - del_phi_2;
    return [del_phi_1, del_phi_2, del_phi_3];
}

const tableElement = document.getElementById(`${containerID}-a`);
const delPSlider = document.getElementById(`${containerID}-del_p-slider`);
const delPOutput = document.getElementById(`${containerID}-del_p-output`);
delPSlider.addEventListener("input", function () {
    const value = parseFloat(delPSlider.value);
    delPOutput.textContent = `${value.toExponential(1)} ${delPOutput.units}`;
    scaleTable.values[0][0] = value;
    scaleTable.update();
});

// Hide loading screen and show main content
const container = document.querySelector(`#${containerID}`);
const loading_screen = container.querySelector("#loading-screen");
const main_content = container.querySelector("#main-content");

loading_screen.style.display = "none";
main_content.style.display = "block";

container.classList.add("dimensional-mode");
