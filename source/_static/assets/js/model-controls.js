// Here we define functions to create various model control elements like sliders

/**
 * Create a slider row. Note the ids should be unique across the document.
 * @param {string} inputID - id for the input element; must be unique across document
 * @param {string} outputID - id for the output element; must be unique across document
 * @param {string} label_text - label text
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
    label_text,
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
    label.innerHTML = label_text;

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
 * @param {string} label_text
 * @param {string} name - Needed for grouping, ignore the linter! Need unique groups across document
 * @param {boolean|null} checked
 * @param {string} value - The value associated with the checkbox
 */
function createCheckbox(id, label_text, name, checked) {
    // Create a wrapper for each individual textbox to hold the box and label
    const checkboxWrapper = document.createElement("span");
    checkboxWrapper.className = "checkbox-button";

    const input = document.createElement("input");
    // Give the id to the input element; thats the thing we care about for controlling our models
    Object.assign(input, { type: "checkbox", id, name });
    input.checked = checked || false;

    const label = document.createElement("label");
    label.setAttribute("for", input.id);
    label.innerHTML = label_text;

    checkboxWrapper.append(input, label);
    return checkboxWrapper;
}

/**
 * Create a checkbox control row
 * @param {string} label_text - label text
 * @param {Array} checkboxes - array of checkboxes
 */
function createCheckboxGroupRow(label_text, checkboxes) {
    const row = document.createElement("div");
    row.className = "control-row";

    // Label for the group
    const groupLabel = document.createElement("label");
    groupLabel.innerHTML = label_text;
    row.appendChild(groupLabel);

    // Container for all checkboxes
    const checkboxContainer = document.createElement("div");
    checkboxContainer.className = "checkbox-group";
    // Append all the checkboxes
    checkboxContainer.append(...checkboxes);
    row.appendChild(checkboxContainer);

    // Apply any additional attributes
    // applyAttributes(config, [row, checkboxContainer], ["className"]);

    return row;
}

/**
 * Create a radio button
 * @param {string} id - id of the radio button; must be unique across document
 * @param {string} label_text
 * @param {string} name - Needed for grouping, ignore the linter! Need unique groups across document
 * @param {boolean|null} checked
 */
function createRadioButton(id, label_text, name, value, checked) {
    const radioWrapper = document.createElement("span");
    radioWrapper.className = "radio-button";

    const input = document.createElement("input");
    Object.assign(input, { type: "radio", value, id, name });
    input.checked = checked || false;

    const label = document.createElement("label");
    label.setAttribute("for", input.id);
    label.innerHTML = label_text;
    radioWrapper.append(input, label);
    return radioWrapper;
}

/**
 * Create a radio button control group row
 * @param {string} label_text - label text
 * @param {Array} buttons - array of radio buttons
 */
function createRadioGroupRow(label_text, buttons) {
    const row = document.createElement("div");
    row.className = "control-row";

    // Label for the group
    const label = document.createElement("label");
    label.innerHTML = label_text;

    // Container for all radio buttons
    const radioContainer = document.createElement("div");
    radioContainer.className = "radio-group";
    radioContainer.append(...buttons);

    row.append(label, radioContainer);

    return row;
}


/**
 * Create coordinate selection control row.
 * @param {string} container_id - The container id to prefix element ids
 * @param {string} starting_coordinates - "non-dimensional" or "dimensional"
 */
function createCoordinateSelectionRow(
    container_id,
    starting_coordinates = "non-dimensional"
) {
    const nonDimButton = createRadioButton(
        `${container_id}-non-dimensional-button`,
        "Non-dimensional",
        `${container_id}-coordinates`,
        "non-dimensional",
        starting_coordinates === "non-dimensional"
    );
    const dimButton = createRadioButton(
        `${container_id}-dimensional-button`,
        "Dimensional",
        `${container_id}-coordinates`,
        "dimensional",
        starting_coordinates === "dimensional"
    );
    return createRadioGroupRow("Coordinates:", [nonDimButton, dimButton]);
}


/**
 * Create overlay toggle checkbox row.
 * @param {string} container_id - The container id to prefix element ids
 */
function createOverlayToggleRow(container_id) {
    const displacementCheckbox = createCheckbox(
        `${container_id}-displacement-checkbox`,
        "Displacement",
        `${container_id}-overlay`,
        false
    );
    const quiverCheckbox = createCheckbox(
        `${container_id}-quiver-checkbox`,
        "Quiver",
        `${container_id}-overlay`,
        true
    );
    const imshowCheckbox = createCheckbox(
        `${container_id}-imshow-checkbox`,
        "Shading",
        `${container_id}-overlay`,
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
 * @param {string} container_id - The container id to prefix element ids
 * @param {Array|null} fields - Array of field names
 * @param {Array|null} labels - Array of corresponding labels
 */
function createImshowSelectionRow(container_id, fields = null, labels = null) {
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

    // Create a list of radio buttons configs
    const buttons = fields.map((field, index) => {
        return createRadioButton(
            `${container_id}-imshow-${field}-button`,
            labels[index] || field,
            `${container_id}-imshow-field`,
            field,
            index === 0 // First button checked by default
        );
    });

    return createRadioGroupRow("Shading:", buttons);
}


/**
 * Create stacked model control rows
 * @param {string} container_id - The unique container id to put all controls in
 * @param {string} starting_coordinates - "non-dimensional" or "dimensional"
 *
 */
function setupCoordinateToggle(
    container_id,
    starting_coordinates = "non-dimensional"
) {
    // Get the container to put all the controls in
    const container = document.getElementById(container_id);

    // Set up radio button listeners to toggle CSS classes on container
    const nonDimRadio = container.querySelector(
        `#${container_id}-non-dimensional-button`
    );
    const dimRadio = container.querySelector(
        `#${container_id}-dimensional-button`
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

const tDimMax = (4 * Math.PI) / Omega; // 48 hours in seconds
const tDimStep = tDimMax * stepRatio;

const fMax = 2 * Omega;
const fValue = 0.5 * Omega;
const fDimStep = fMax * stepRatio;

const alphaMin = 1e-2 * Omega;
const alphaMax = 2 * Omega;
const alphaValue = 0.2 * Omega;
const alphaDimStep = (alphaMax - alphaMin) * stepRatio;

const NMin = 1e-1 * Omega;
const NMax = (0.1 / Omega) * Omega;
const NValue = (1e-2 / Omega) * Omega;
const NDimStep = (NMax - NMin) * stepRatio;

const HValue = 1e3;

/**
 * Convenience function to build default slider control rows for dimensional coordinates.
 * @param {string} container_id - The unique container id to prefix element ids
 * @returns {{tDimSlider: HTMLDivElement, fSlider: HTMLDivElement, alphaSlider: HTMLDivElement, NSlider: HTMLDivElement, HSlider: HTMLDivElement, Q0Slider: HTMLDivElement}}
 */
function coreWaveSlidersDim(container_id) {
    const className = "dimensional";
    tDimSlider = createSliderRow(
        `${container_id}-t_dim-slider`,
        `${container_id}-t_dim-output`,
        "\\(t:\\)",
        0,
        tDimMax,
        0.0,
        tDimStep,
        className,
        "s"
    );
    fSlider = createSliderRow(
        `${container_id}-f-slider`,
        `${container_id}-f-output`,
        "\\(f:\\)",
        0,
        fMax,
        0.5 * Omega,
        fDimStep,
        className,
        "s⁻¹"
    );
    alphaSlider = createSliderRow(
        `${container_id}-alpha-slider`,
        `${container_id}-alpha-output`,
        "\\(\\alpha:\\)",
        alphaMin,
        alphaMax,
        alphaValue,
        alphaDimStep,
        className,
        "s⁻¹"
    );
    NSlider = createSliderRow(
        `${container_id}-N-slider`,
        `${container_id}-N-output`,
        "\\(N:\\)",
        NMin,
        NMax,
        NValue,
        NDimStep,
        className,
        "s⁻¹"
    );
    HSlider = createSliderRow(
        `${container_id}-H-slider`,
        `${container_id}-H-output`,
        "\\(H:\\)",
        100,
        5e3,
        HValue,
        100,
        className,
        "m"
    );
    Q0Slider = createSliderRow(
        `${container_id}-Q_0-slider`,
        `${container_id}-Q_0-output`,
        "\\(Q_0:\\)",
        1e-6,
        10e-5,
        1.2e-5,
        1e-6,
        className,
        "m s⁻³"
    );
    return { tDimSlider, fSlider, alphaSlider, NSlider, HSlider, Q0Slider };
}


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

/**
 * Convenience function to build default slider control rows for non-dimensional coordinates.
 * @param {string} container_id - The unique container id to prefix element ids
 * @returns {{tSlider: HTMLDivElement, fOmegaSlider: HTMLDivElement, alphaOmegaSlider: HTMLDivElement, NOmegaSlider: HTMLDivElement}}
 */
function coreWaveSlidersNonDim(container_id) {
    const className = "non-dimensional";
    tSlider = createSliderRow(
        `${container_id}-t-slider`,
        `${container_id}-t-output`,
        "\\(t:\\)",
        0,
        tNonDimMax,
        0.0,
        tNonDimStep,
        className
    );
    fOmegaSlider = createSliderRow(
        `${container_id}-f_omega-slider`,
        `${container_id}-f_omega-output`,
        "\\(f / \\omega :\\)",
        0,
        fOmMax,
        fOmValue,
        fOmNonDimStep,
        className
    );
    alphaOmegaSlider = createSliderRow(
        `${container_id}-alpha_omega-slider`,
        `${container_id}-alpha_omega-output`,
        "\\(\\alpha / \\omega :\\)",
        alOmMin,
        alOmMax,
        alOmValue,
        alOmNonDimStep,
        className
    );
    NOmegaSlider = createSliderRow(
        `${container_id}-N_omega-slider`,
        `${container_id}-N_omega-output`,
        "\\(N / \\omega :\\)",
        NOmegaMin,
        NOmegaMax,
        NOmegaValue,
        NOmNonDimStep,
        className
    );
    return { tSlider, fOmegaSlider, alphaOmegaSlider, NOmegaSlider };
}


/**
 * Main function to create all wave config with coordinate toggle
 */
function coreWaveConfigs(overrides = {}) {
    return [
        ...coreWaveConfigsNonDim(overrides),
        ...coreWaveConfigsDim(overrides),
    ];
}
