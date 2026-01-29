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
 * @param {number} L - Horizontal length scale
 * @param {number} U - Horizontal velocity scale
 * @param {number} W - Vertical velocity scale
 * @param {number} P_bar - Base state pressure scale
 * @param {number} R_bar - Base state density scale
 * @returns {number[]} - Array with inferred scales
 */
function inferredScales(L, U, W, P_bar, R_bar) {
    const T = L / U;
    const H = W * T;

    // Infer Del_P from horizontal momentum equation
    const Del_P = Math.max(R_bar * U ** 2, R_bar * f * U * L);

    // Infer Del_R from vertical momentum equation
    const Del_R = Math.max((W * R_bar) / (g * T), Del_P / (g * H));

    if (Del_P > P_bar || Del_R > R_bar) {
        return [null, null, null, null, null];
    }

    // Buoyancy Scale
    const Del_Phi =
        (1 / gamma) * Math.log((P_bar + Del_P) / P_bar) -
        Math.log((R_bar + Del_R) / R_bar);

    return [T, H, Del_P, Del_R, Del_Phi];
}

/**
 * Calculate the terms for the scale analysis table
 * @param {number} L - Horizontal length scale
 * @param {number} U - Horizontal velocity scale
 * @param {number} W - Vertical velocity scale
 * @param {number} P_bar - Base state pressure scale
 * @param {number} R_bar - Base state density scale
 * @returns {Array} - 2D array of table values
 */
function calculateTableValues(L, U, W, P_bar, R_bar) {
    // Implied Scales
    const [T, H, Del_P, Del_R, Del_Phi] = inferredScales(L, U, W, P_bar, R_bar);

    if ([T, H, Del_P, Del_R, Del_Phi].some((x) => x === null)) {
        // Handle the null case
        return [
            [null, null, null, null],
            [null, null, null, null],
            [null, null, null, null],
        ];
    }

    // Residuals
    const Del_Phi_1 = (1 / gamma) * (Del_P / P_bar);
    const Del_Phi_2 = -(Del_R / R_bar);
    const R_1 = (1 / gamma) * Math.log((P_bar + Del_P) / P_bar) - Del_Phi_1;
    const R_2 = -Math.log((R_bar + Del_R) / R_bar) - Del_Phi_2;
    const R_3 = 1 / (R_bar + Del_R) - 1 / R_bar;
    const R_4 = -g * R_1 - g * R_2 + R_3 * (-Del_P / H - g * Del_R);

    const u_mom_terms = [
        U / T,
        f * U,
        (1 / R_bar) * (Del_P / L),
        (R_3 * Del_P) / L,
    ];
    const w_mom_terms = [W / T, g * Del_Phi, Del_P / R_bar / H, R_4];
    const cont_terms = [Del_R / T, R_bar / T, R_bar / T, Del_R / T];

    return [u_mom_terms, w_mom_terms, cont_terms];
}

// Create container for the table
let tableIndentifer = `#${containerID} #main-content #scale-table`;
const table_container = document.querySelector(tableIndentifer);

// Create sliders to control scales. Note sliders are logarithmic, but values
// stored in scaleTable are linear.

args = [`${containerID}-P_bar-slider`, `${containerID}-P_bar-output`];
// 1e5 Pa = 1000 hPa = 1 bar
args.push("\\(\\overline{P}:\\)", 4, 6, 5);
args.push(0.1, null, "Pa");
const PBarSliderRow = createSliderRow(...args);

args = [`${containerID}-R_bar-slider`, `${containerID}-R_bar-output`];
args.push("\\(\\overline{R}:\\)", -3, 0.5, 0, 0.1);
args.push(null, "kg m<sup>-3</sup>");
const RBarSliderRow = createSliderRow(...args);

args = [`${containerID}-U-slider`, `${containerID}-U-output`];
args.push("\\(U:\\)", -3, 2, 1, 0.1);
args.push(null, "m s<sup>−1</sup>");
const USliderRow = createSliderRow(...args);

args = [`${containerID}-W-slider`, `${containerID}-W-output`];
args.push("\\(W:\\)", -3, 2, 1, 0.1);
args.push(null, "m s<sup>−1</sup>");
const WSliderRow = createSliderRow(...args);

args = [`${containerID}-L-slider`, `${containerID}-L-output`];
args.push("\\(L:\\)", -3, 6, 3, 0.1);
args.push(null, "m");
const LSliderRow = createSliderRow(...args);

allSliders = [LSliderRow, USliderRow, WSliderRow, PBarSliderRow, RBarSliderRow];
// Fix the initial slider outputs for exponential formatting
initializeOutputs(allSliders);

const initialSliderValues = allSliders.map(
    (slider) => 10 ** slider.querySelector("input").value
);

// Now append all the slider rows to the controls container
let controlsIdentifier = `#${containerID} #main-content #controls`;
const controls = document.querySelector(controlsIdentifier);
controls.append(...allSliders);

// Build the scale table
initialTableValues = calculateTableValues(...initialSliderValues);
initialInferredScaleValues = inferredScales(...initialSliderValues);
const zPressureGradientForce =
    "-\\frac{\\partial }{\\partial z}" +
    "\\left(\\frac{\\delta p}{\\overline{\\rho}}\\right)";
const scaleTable = new ScaleTable(
    containerID,
    [
        [
            "\\frac{D \\mathbf{u}}{D t}",
            "f\\mathbf{k}\\times \\mathbf{u}",
            "-\\frac{1}{\\overline{\\rho}} \\nabla_h \\delta p",
            "R_3 \\nabla_h \\delta p",
        ],
        ["\\frac{D w}{D t}", "g\\delta \\phi", zPressureGradientForce, "R_4"],
        [
            "\\frac{\\partial \\delta \\rho}{\\partial t}",
            "\\nabla_h \\cdot (\\overline{\\rho} \\mathbf{u})",
            "\\frac{\\partial }{\\partial z}(\\overline{\\rho} w)",
            "\\nabla \\cdot (\\delta \\rho \\mathbf{v})",
        ],
    ],
    initialTableValues,
    [
        ["m s<sup>-2</sup>"],
        ["m s<sup>-2</sup>"],
        ["kg m<sup>-3</sup> s<sup>-1</sup>"],
    ],
    ["T", "H", "\\Delta P", "\\Delta R", "\\Delta \\Phi"],
    initialInferredScaleValues,
    ["s", "m", "Pa", "kg m<sup>-3</sup>", ""]
);
table_container.append(scaleTable.table, scaleTable.inferredScalesDiv);

// Setup the listeners
let sliderIDs = [`${containerID}-L-slider`, `${containerID}-U-slider`];
sliderIDs.push(`${containerID}-W-slider`);
sliderIDs.push(`${containerID}-P_bar-slider`);
sliderIDs.push(`${containerID}-R_bar-slider`);

addListeners(sliderIDs, inferredScales, calculateTableValues, scaleTable);

// Hide loading screen and show main content
const container = document.querySelector(`#${containerID}`);
const loading_screen = container.querySelector("#loading-screen");
const main_content = container.querySelector("#main-content");

loading_screen.style.display = "none";
main_content.style.display = "block";

container.classList.add("dimensional-mode");
