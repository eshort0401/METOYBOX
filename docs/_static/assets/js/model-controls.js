// Here we define functions to create various model control elements like sliders

/**
 * Create a slider row. Note the ids should be unique across the document.
 * @param {string} inputID - id for the input element; must be unique across document
 * @param {string} outputID - id for the output element; must be unique across document
 * @param {string} labelText - label text
 * @param {number} min - Min slider value
 * @param {number} max - Max slider value
 * @param {number} value - Initial value
 * @param {number} step - Slider step
 * @param {string|null} className - Optional CSS class
 * @param {string|null} units - Optional units for display
 */
function createSliderRow(
    inputID,
    outputID,
    labelText,
    min,
    max,
    value,
    step,
    className = null,
    units = null
) {
    // Create a div to store the control row
    const row = document.createElement("div");
    row.classList.add("control-row");

    // Add class name if provided
    if (className) {
        row.classList.add(className);
    }

    // Create label
    const label = document.createElement("label");
    label.innerHTML = labelText;

    // Create slider itself
    const input = document.createElement("input");
    // Apply relevant attributes to slider input.
    Object.assign(input, { type: "range", min, max, step, value, id: inputID });

    // Output
    const output = document.createElement("output");
    output.id = outputID;
    output.textContent = formatOutput(value, units, step);
    output.units = units || "";

    // Reminder; append creates nested html elements inside the parent
    row.append(label, input, output);

    return row;
}

/**
 * Format slider outputs neatly
 */
function formatOutput(value, units, step) {
    if (units) {
        return `${parseFloat(value).toExponential(1)} ${units}`;
    } else {
        const decimals = Math.max(0, -Math.floor(Math.log10(step)));
        return `${parseFloat(value).toFixed(decimals)}`;
    }
}

/**
 * Create a checkbox
 * @param {string} id - Must be unique across document
 * @param {string} labelText
 * @param {string} name - Needed for grouping, ignore the linter! Need unique groups across document
 * @param {boolean|null} checked
 * @param {string} value - The value associated with the checkbox
 */
function createCheckbox(id, labelText, name, checked) {
    // Create a wrapper for each individual textbox to hold the box and label
    const checkboxWrapper = document.createElement("span");
    checkboxWrapper.className = "checkbox-button";

    const input = document.createElement("input");
    // Give the id to the input element; thats the thing we care about for controlling our models
    Object.assign(input, { type: "checkbox", id, name });
    input.checked = checked || false;

    const label = document.createElement("label");
    label.setAttribute("for", input.id);
    label.innerHTML = labelText;

    checkboxWrapper.append(input, label);
    return checkboxWrapper;
}

/**
 * Create a checkbox control row
 * @param {string} labelText - label text
 * @param {Array} checkboxes - array of checkboxes
 */
function createCheckboxGroupRow(labelText, checkboxes) {
    const row = document.createElement("div");
    row.className = "control-row";

    // Label for the group
    const groupLabel = document.createElement("label");
    groupLabel.innerHTML = labelText;
    row.appendChild(groupLabel);

    // Container for all checkboxes
    const checkboxContainer = document.createElement("div");
    checkboxContainer.className = "checkbox-group";
    // Append all the checkboxes
    checkboxContainer.append(...checkboxes);
    row.appendChild(checkboxContainer);

    return row;
}

/**
 * Create a radio button
 * @param {string} id - id of the radio button; must be unique across document
 * @param {string} labelText
 * @param {string} name - Needed for grouping, ignore the linter! Need unique groups across document
 * @param {boolean|null} checked
 * @param {string|null} nonDimLabelText - Optional label text for non-dimensional mode
 */
function createRadioButton(
    id,
    labelText,
    name,
    value,
    checked,
    nonDimLabelText = null
) {
    const radioWrapper = document.createElement("span");
    radioWrapper.className = "radio-button";
    if (nonDimLabelText === null) {
        nonDimLabelText = labelText;
    }

    const input = document.createElement("input");
    Object.assign(input, { type: "radio", value, id, name });
    input.checked = checked || false;

    const dimLabel = document.createElement("label");
    dimLabel.setAttribute("for", input.id);
    dimLabel.className = "dimensional";
    // Initialize to the dimensional label
    dimLabel.innerHTML = labelText;

    const nonDimLabel = document.createElement("label");
    nonDimLabel.setAttribute("for", input.id);
    nonDimLabel.className = "non-dimensional";
    nonDimLabel.innerHTML = nonDimLabelText;

    radioWrapper.append(input, dimLabel, nonDimLabel);
    return radioWrapper;
}

/**
 * Create a radio button control group row
 * @param {string} labelText - label text
 * @param {Array} buttons - array of radio buttons
 */
function createRadioGroupRow(labelText, buttons) {
    const row = document.createElement("div");
    row.className = "control-row";

    // Label for the group
    const label = document.createElement("label");
    label.innerHTML = labelText;

    // Container for all radio buttons
    const radioContainer = document.createElement("div");
    radioContainer.className = "radio-group";
    radioContainer.append(...buttons);

    row.append(label, radioContainer);

    return row;
}

/**
 * Create coordinate selection control row.
 * @param {string} containerID - The container id to prefix element ids
 * @param {string} starting_coordinates - "non-dimensional" or "dimensional"
 */
function createCoordinateSelectionRow(
    containerID,
    starting_coordinates = "non-dimensional"
) {
    const nonDimButton = createRadioButton(
        `${containerID}-non-dimensional-button`,
        "Non-dimensional",
        `${containerID}-coordinates`,
        "non-dimensional",
        starting_coordinates === "non-dimensional"
    );
    const dimButton = createRadioButton(
        `${containerID}-dimensional-button`,
        "Dimensional",
        `${containerID}-coordinates`,
        "dimensional",
        starting_coordinates === "dimensional"
    );
    return createRadioGroupRow("Coordinates:", [nonDimButton, dimButton]);
}

/**
 * Create overlay toggle checkbox row.
 * @param {string} containerID - The container id to prefix element ids
 */
function createOverlayToggleRow(containerID) {
    const displacementCheckbox = createCheckbox(
        `${containerID}-displacement-checkbox`,
        "Displacement",
        `${containerID}-overlay`,
        false
    );
    const quiverCheckbox = createCheckbox(
        `${containerID}-quiver-checkbox`,
        "Arrows",
        `${containerID}-overlay`,
        true
    );
    const imshowCheckbox = createCheckbox(
        `${containerID}-imshow-checkbox`,
        "Shading",
        `${containerID}-overlay`,
        true
    );
    return createCheckboxGroupRow("Show:", [
        displacementCheckbox,
        quiverCheckbox,
        imshowCheckbox,
    ]);
}

/**
 * Create imshow field selection radio button group
 * @param {string} containerID - The container id to prefix element ids
 * @param {Array|null} fields - Array of field names
 * @param {Array|null} labels - Array of corresponding labels
 * @param {string} feature - Feature name - imshow, quiver, displacement
 */
function createFieldSelectionRow(
    containerID,
    fields = null,
    labels = null,
    feature = "imshow",
    nonDimLabels = null
) {
    // Set default fields and labels if not provided
    if (fields === null) {
        fields = ["psi", "u", "v", "w", "Q", "phi"];
    }
    if (labels === null) {
        labels = [
            "\\(\\psi\\)",
            "\\(u\\)",
            "\\(v\\)",
            "\\(w\\)",
            "\\(Q\\)",
            "\\(\\phi\\)",
        ];
    }
    if (nonDimLabels === null) {
        nonDimLabels = labels;
    }

    // Create a list of radio buttons configs
    const buttons = fields.map((field, index) => {
        return createRadioButton(
            `${containerID}-${feature}-${field}-button`,
            labels[index] || field,
            `${containerID}-${feature}-field`,
            field,
            index === 0, // First button checked by default
            nonDimLabels[index] || labels[index] || field
        );
    });

    const label = { imshow: "Shading:", quiver: "Arrows:" };
    return createRadioGroupRow(label[feature] || "Shading:", buttons);
}

/**
 * Create stacked model control rows
 * @param {string} containerID - The unique container id to put all controls in
 * @param {string} starting_coordinates - "non-dimensional" or "dimensional"
 *
 */
function setupCoordinateToggle(
    containerID,
    starting_coordinates = "non-dimensional"
) {
    // Get the container to put all the controls in
    const container = document.getElementById(containerID);

    // Set up radio button listeners to toggle CSS classes on container
    const nonDimRadio = container.querySelector(
        `#${containerID}-non-dimensional-button`
    );
    const dimRadio = container.querySelector(
        `#${containerID}-dimensional-button`
    );

    if (nonDimRadio)
        nonDimRadio.addEventListener("change", () => {
            if (nonDimRadio.checked) {
                container.classList.remove("dimensional-mode");
                container.classList.add("non-dimensional-mode");
            }
        });

    if (dimRadio)
        dimRadio.addEventListener("change", () => {
            if (dimRadio.checked) {
                container.classList.remove("non-dimensional-mode");
                container.classList.add("dimensional-mode");
            }
        });

    // Set initial state
    container.classList.add(starting_coordinates + "-mode");

    // Re-render MathJax once for all elements
    if (window.MathJax && window.MathJax.typesetPromise) {
        MathJax.typesetPromise([container]).catch((err) => console.log(err));
    }
}

// Setup variables and steps to help ensure dimensional and non-dimensional sliders match up
const Omega = (2 * Math.PI) / (24 * 3600); // diurnal frequency in radians per second
const stepRatio = 5e-3; // Step as a ratio of the quantity's scale
const HValue = 1e3;
const alphaValue = 0.2 * Omega;
const NValue = 1e-2;
const MDimValue = Omega * 1e2;
const xScale = (NValue * HValue) / Omega;

const tDimMax = (4 * Math.PI) / Omega; // 48 hours in seconds
const tDimStep = tDimMax * stepRatio;

// Create some convenience functions to build commonly used sliders
function getTDimSlider(containerID) {
    return createSliderRow(
        `${containerID}-t_dim-slider`,
        `${containerID}-t_dim-output`,
        "\\(t:\\)",
        0,
        tDimMax,
        0.0,
        tDimStep,
        "dimensional",
        "s"
    );
}

const fMax = 2 * Omega;
const fValue = 0.5 * Omega;
const fDimStep = fMax * stepRatio;

function getFSlider(containerID) {
    return createSliderRow(
        `${containerID}-f-slider`,
        `${containerID}-f-output`,
        "\\(f:\\)",
        0,
        fMax,
        0.5 * Omega,
        fDimStep,
        "dimensional",
        "s⁻¹"
    );
}

const alphaMin = 1e-2 * Omega;
const alphaMax = 2 * Omega;
const alphaDimStep = (alphaMax - alphaMin) * stepRatio;

function getAlphaSlider(containerID) {
    return createSliderRow(
        `${containerID}-alpha-slider`,
        `${containerID}-alpha-output`,
        "\\(\\alpha:\\)",
        alphaMin,
        alphaMax,
        alphaValue,
        alphaDimStep,
        "dimensional",
        "s⁻¹"
    );
}

const NMin = 1e-3;
const NMax = 2e-1;
const NDimStep = (NMax - NMin) * stepRatio;

function getNSlider(containerID) {
    return createSliderRow(
        `${containerID}-N-slider`,
        `${containerID}-N-output`,
        "\\(N:\\)",
        NMin,
        NMax,
        NValue,
        NDimStep,
        "dimensional",
        "s⁻¹"
    );
}

function getHSlider(containerID) {
    return createSliderRow(
        `${containerID}-H-slider`,
        `${containerID}-H-output`,
        "\\(H:\\)",
        100,
        5e3,
        HValue,
        100,
        "dimensional",
        "m"
    );
}

const Q0Min = 1e-6;
const Q0Max = 3.6e-5;
const Q0Value = 1.2e-5;
const Q0Step = (Q0Max - Q0Min) * stepRatio;

function getQ0Slider(containerID) {
    return createSliderRow(
        `${containerID}-Q_0-slider`,
        `${containerID}-Q_0-output`,
        "\\(Q_0:\\)",
        Q0Min,
        Q0Max,
        Q0Value,
        Q0Step,
        "dimensional",
        "m s⁻³"
    );
}

const LDimMin = 0.01 * xScale;
const LDimMax = 1 * xScale;
const LDimValue = 0.2 * xScale;
const LDimStep = (LDimMax - LDimMin) * stepRatio;

function getLDimSlider(containerID) {
    return createSliderRow(
        `${containerID}-L_dim-slider`,
        `${containerID}-L_dim-output`,
        "\\(L:\\)",
        LDimMin,
        LDimMax,
        LDimValue,
        LDimStep,
        "dimensional",
        "m"
    );
}

function getOmegaSlider(containerID) {
    return createSliderRow(
        `${containerID}-omega-slider`,
        `${containerID}-omega-output`,
        "\\(\\omega:\\)",
        Omega * stepRatio,
        2 * Omega,
        Omega,
        Omega * stepRatio,
        "dimensional",
        "s⁻¹"
    );
}

const kScale = 1 / xScale;
const kMinDim = 0.1 * kScale;
const kMaxDim = 10 * Math.PI * kScale;
const kValueDim = Math.PI * kScale;
const kStepDim = (kMaxDim - kMinDim) * stepRatio;

function getKDimSlider(containerID) {
    return createSliderRow(
        `${containerID}-k_dim-slider`,
        `${containerID}-k_dim-output`,
        "\\(k:\\)",
        kStepDim,
        kMaxDim,
        kValueDim,
        kStepDim,
        "dimensional",
        "m⁻¹"
    );
}

const sigmaDimMin = 0.1 * Omega;
const sigmaDimMax = 5 * Omega;
const sigmaDimStep = (sigmaDimMax - sigmaDimMin) * stepRatio;

function getSigmaDimSlider(containerID) {
    return createSliderRow(
        `${containerID}-sigma_dim-slider`,
        `${containerID}-sigma_dim-output`,
        "\\(\\sigma:\\)",
        sigmaDimMin,
        sigmaDimMax,
        Omega,
        sigmaDimStep,
        "dimensional",
        "s⁻¹"
    );
}

const zFDimMin = 0.1;
const zFDimMax = 3e3;
const zFDimValue = 1e3;
const zFDimStep = 3 * stepRatio;

function getZfDimSlider(containerID) {
    return createSliderRow(
        `${containerID}-z_f_dim-slider`,
        `${containerID}-z_f_dim-output`,
        "\\(z_f:\\)",
        zFDimMin,
        zFDimMax,
        zFDimValue,
        zFDimStep,
        "dimensional",
        "m"
    );
}

const MMaxDim = 1e-2;
const MStepDim = MMaxDim * stepRatio;

function getMDimSlider(containerID) {
    return createSliderRow(
        `${containerID}-M_dim-slider`,
        `${containerID}-M_dim-output`,
        "\\(M:\\)",
        0,
        MMaxDim,
        MDimValue,
        MStepDim,
        "dimensional",
        "m m⁻¹"
    );
}

/**
 * Convenience function to build default slider control rows for dimensional coordinates.
 * @param {string} containerID - The unique container id to prefix element ids
 * @returns {{tDimSlider: HTMLDivElement, fSlider: HTMLDivElement, alphaSlider: HTMLDivElement, NSlider: HTMLDivElement, HSlider: HTMLDivElement, Q0Slider: HTMLDivElement}}
 */
function coreWaveSlidersDim(containerID) {
    const tDimSlider = getTDimSlider(containerID);
    const fSlider = getFSlider(containerID);
    const alphaSlider = getAlphaSlider(containerID);
    const NSlider = getNSlider(containerID);
    const HSlider = getHSlider(containerID);
    const Q0Slider = getQ0Slider(containerID);
    return { tDimSlider, fSlider, alphaSlider, NSlider, HSlider, Q0Slider };
}

// Default slider configurations for non-dimensional sliders
const tNonDimMax = tDimMax * Omega; // Non-dimensional max time
const tNonDimStep = tNonDimMax * stepRatio;

const NOmegaMin = NMin / Omega;
const NOmegaMax = NMax / Omega;
const NOmegaValue = NValue / Omega;
const NOmNonDimStep = (NOmegaMax - NOmegaMin) * stepRatio;

const fOmMax = fMax / Omega;
const fOmValue = fValue / Omega;
const fOmNonDimStep = fOmMax * stepRatio;

const alOmMin = alphaMin / Omega;
const alOmMax = alphaMax / Omega;
const alOmValue = alphaValue / Omega;
const alOmNonDimStep = (alOmMax - alOmMin) * stepRatio;

const sigmaMin = sigmaDimMin / Omega;
const sigmaMax = sigmaDimMax / Omega;
const sigmaStep = (sigmaMax - sigmaMin) * stepRatio;

const kMin = kMinDim / kScale;
const kMax = kMaxDim / kScale;
const kStep = (kMax - kMin) * stepRatio;
const kValue = kValueDim / kScale;

const MStep = 3 * stepRatio;

function getTNonDimSlider(containerID) {
    return createSliderRow(
        `${containerID}-t-slider`,
        `${containerID}-t-output`,
        "\\(t:\\)",
        0,
        tNonDimMax,
        0.0,
        tNonDimStep,
        "non-dimensional"
    );
}

function getFNonDimSlider(containerID) {
    return createSliderRow(
        `${containerID}-f_omega-slider`,
        `${containerID}-f_omega-output`,
        "\\(f / \\omega :\\)",
        0,
        fOmMax,
        fOmValue,
        fOmNonDimStep,
        "non-dimensional"
    );
}

function getAlphaNonDimSlider(containerID) {
    return createSliderRow(
        `${containerID}-alpha_omega-slider`,
        `${containerID}-alpha_omega-output`,
        "\\(\\alpha / \\omega :\\)",
        alOmMin,
        alOmMax,
        alOmValue,
        alOmNonDimStep,
        "non-dimensional"
    );
}

function getNNonDimSlider(containerID) {
    return createSliderRow(
        `${containerID}-N_omega-slider`,
        `${containerID}-N_omega-output`,
        "\\(N / \\omega :\\)",
        NOmegaMin,
        NOmegaMax,
        NOmegaValue,
        NOmNonDimStep,
        "non-dimensional"
    );
}

function getLNonDimSlider(containerID) {
    return createSliderRow(
        `${containerID}-L-slider`,
        `${containerID}-L-output`,
        "\\(L:\\)",
        LDimMin / xScale,
        LDimMax / xScale,
        LDimValue / xScale,
        LDimStep / xScale,
        "non-dimensional"
    );
}

function getZfNonDimSlider(containerID) {
    return createSliderRow(
        `${containerID}-z_f-slider`,
        `${containerID}-z_f-output`,
        "\\(z_f:\\)",
        zFDimMin / HValue,
        zFDimMax / HValue,
        zFDimValue / HValue,
        zFDimStep / HValue,
        "non-dimensional"
    );
}

function getKNonDimSlider(containerID) {
    return createSliderRow(
        `${containerID}-k-slider`,
        `${containerID}-k-output`,
        "\\(k:\\)",
        kStep,
        kMax,
        kValue,
        kStep,
        "non-dimensional"
    );
}

function getSigmaNonDimSlider(containerID) {
    return createSliderRow(
        `${containerID}-sigma-slider`,
        `${containerID}-sigma-output`,
        "\\(\\sigma:\\)",
        sigmaMin,
        sigmaMax,
        1,
        sigmaStep,
        "non-dimensional"
    );
}

function getMNonDimSlider(containerID) {
    return createSliderRow(
        `${containerID}-M-slider`,
        `${containerID}-M-output`,
        "\\(M:\\)",
        0,
        3,
        0.2,
        MStep,
        "non-dimensional"
    );
}

/**
 * Convenience function to build default slider control rows for non-dimensional coordinates.
 * @param {string} containerID - The unique container id to prefix element ids
 * @returns {{tSlider: HTMLDivElement, fOmegaSlider: HTMLDivElement, alphaOmegaSlider: HTMLDivElement, NOmegaSlider: HTMLDivElement}}
 */
function coreWaveSlidersNonDim(containerID) {
    const tSlider = getTNonDimSlider(containerID);
    const fOmegaSlider = getFNonDimSlider(containerID);
    const alphaOmegaSlider = getAlphaNonDimSlider(containerID);
    const NOmegaSlider = getNNonDimSlider(containerID);
    return { tSlider, fOmegaSlider, alphaOmegaSlider, NOmegaSlider };
}
