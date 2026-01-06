// Setup constants
const c_p = 1005; // J kg^-1 K^-1
const c_v = 718; // J kg^-1 K^-1
const gamma = c_p / c_v;
const R = c_p - c_v; // J kg^-1 K^-1
const g = 9.81; // m s^-2
const Omega = (2 * Math.PI) / (24 * 3600); // rad s^-1
const f = Omega;

// Define reference values
const p_s = 1e5; // Pa
const T_s = 300; // K
const rho_s = p_s / (R * T_s); // Ideal gas law

/**
 * Calculate the terms for the scale analysis table
 * @param {number} del_p
 * @param {number} p_bar
 * @param {number} del_rho
 * @param {number} rho_bar
 * @returns
 */
function calculateTableValues(del_p, p_bar, del_rho, rho_bar, L, H, T) {
    const del_phi =
        (1 / gamma) * Math.log((p_bar + del_p) / p_bar) -
        Math.log((rho_bar + del_rho) / rho_bar);
    const del_phi_1 = (1 / gamma) * (del_p / p_bar);
    const del_phi_2 = -(del_rho / rho_bar);
    const R_1 = (1 / gamma) * Math.log((p_bar + del_p) / p_bar) - del_phi_1;
    const R_2 = -Math.log((rho_bar + del_rho) / rho_bar) - del_phi_2;

    const R_3 = 1 / (rho_bar + del_rho) - 1 / rho_bar;

    // Hmm... if the length, time, density and pressure scales are specified, I suspect the height
    // scale will follow from the continuity equation.

    U = L / T;
    W = H / T;

    u_mom_terms = [
        U / T,
        U * (U / L),
        W * (U / H),
        f * U,
        (1 / rho_bar) * (del_p / L),
        (R_3 * del_p) / L,
        null,
    ];
    w_mom_terms = [
        W / T,
        U * (W / L),
        W * (W / H),
        g * del_phi,
        del_p / rho_bar / H,
        g * R_1,
        g * R_2,
    ];

    return [u_mom_terms, w_mom_terms];
}

// Create container for the table
let tableIndentifer = `#${containerID} #main-content #scale-table`;
const table_container = document.querySelector(tableIndentifer);

// Create sliders to control scales. Note sliders are logarithmic, but values
// stored in scaleTable are linear.

// Store the initial exponents and values for each slider
const initialExponents = [4, 5, -1, 0, 4, 4, 3];
const initialSliderValues = initialExponents.map((exp) => Math.pow(10, exp));

// 1e3 Pa = 10 hPa
let args = [`${containerID}-del_p-slider`, `${containerID}-del_p-output`];
args.push("\\(\\delta p:\\)", 0, 6, initialExponents[0]);
args.push(0.1, null, "Pa");
const delPSliderRow = createSliderRow(...args);

args = [`${containerID}-p_bar-slider`, `${containerID}-p_bar-output`];
// 1e5 Pa = 1000 hPa = 1 bar
args.push("\\(\\overline{p}:\\)", 0, 6, initialExponents[1]);
args.push(0.1, null, "Pa");
const pBarSliderRow = createSliderRow(...args);

args = [`${containerID}-del_rho-slider`, `${containerID}-del_rho-output`];
args.push("\\(\\delta \\rho:\\)", -3, 0.5, initialExponents[2], 0.1);
args.push(null, "kg m⁻³");
const delRhoSliderRow = createSliderRow(...args);

args = [`${containerID}-rho_bar-slider`, `${containerID}-rho_bar-output`];
args.push("\\(\\overline{\\rho}:\\)", -3, 0.5, initialExponents[3], 0.1);
args.push(null, "kg m⁻³");
const rhoBarSliderRow = createSliderRow(...args);

args = [`${containerID}-L-slider`, `${containerID}-L-output`];
args.push("\\(L:\\)", -3, 6, initialExponents[4], 0.1);
args.push(null, "m");
const LSliderRow = createSliderRow(...args);

args = [`${containerID}-H-slider`, `${containerID}-H-output`];
args.push("\\(H:\\)", -3, 6, initialExponents[5], 0.1);
args.push(null, "m");
const HSliderRow = createSliderRow(...args);

args = [`${containerID}-T-slider`, `${containerID}-T-output`];
args.push("\\(T:\\)", -3, 6, initialExponents[5], 0.1);
args.push(null, "s");
const TSliderRow = createSliderRow(...args);

let allSliders = [delPSliderRow, pBarSliderRow, delRhoSliderRow];
allSliders.push(rhoBarSliderRow, LSliderRow, HSliderRow, TSliderRow);
// Fix the initial slider output formats
initializeValues(allSliders);

// Now append all the slider rows to the controls container
let controlsIdentifier = `#${containerID} #main-content #controls`;
const controls = document.querySelector(controlsIdentifier);
controls.append(...allSliders);

// Build the scale table
const initialTableValues = calculateTableValues(...initialSliderValues);
const scaleTable = new ScaleTable(
    containerID,
    [
        [
            "\\frac{\\partial \\mathbf{u}}{\\partial t}",
            "\\mathbf{u} \\cdot \\nabla_h \\mathbf{u}",
            "w \\frac{\\partial \\mathbf{u}}{\\partial z}",
            "f\\mathbf{k}\\times \\mathbf{u}",
            "-\\frac{1}{\\overline{\\rho}} \\nabla_h \\delta p",
            "R_3 \\nabla_h \\delta p",
            "",
        ],
        ["a", "x", "y", "b", "c", "d", "e"],
    ],
    initialTableValues,
    [
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
    ] // Everything unitless in this case
);
scaleTable.id = `${containerID}-scale-table`;
table_container.appendChild(scaleTable.table);

// Setup the listeners
let sliderIDs = [`${containerID}-del_p-slider`, `${containerID}-p_bar-slider`];
sliderIDs.push(`${containerID}-del_rho-slider`);
sliderIDs.push(`${containerID}-rho_bar-slider`);
sliderIDs.push(`${containerID}-L-slider`, `${containerID}-H-slider`);
sliderIDs.push(`${containerID}-T-slider`);

addListeners(sliderIDs, calculateTableValues, scaleTable);

// Hide loading screen and show main content
const container = document.querySelector(`#${containerID}`);
const loading_screen = container.querySelector("#loading-screen");
const main_content = container.querySelector("#main-content");

loading_screen.style.display = "none";
main_content.style.display = "block";

container.classList.add("dimensional-mode");
