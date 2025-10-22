/**
 * Create a slider row
 */
function createSliderRow(config) {
    const row = document.createElement("div");
    row.classList.add("control-row");
    // row.classList.add(config.className);
    if (config.className) {
        row.classList.add(config.className);
    }

    // Label
    const label = document.createElement("label");
    label.innerHTML = config.label;
    row.appendChild(label);

    // Slider
    const input = document.createElement("input");
    input.type = "range";
    applyConfigAttributes(config, [input], ["id", "min", "max", "step"]);
    row.appendChild(input);

    // Set value after appending to fix annoying bug
    input.value = config.value;

    // Output
    const output = document.createElement("output");
    output.id = config.id.replace("-slider", "-out");
    output.textContent = formatOutput(config.value, config.units, config.step);
    output.units = config.units || "";
    row.appendChild(output);

    return row;
}

/**
 * Format slider outputs neatly
 */
function formatOutput(value, units, step) {
    if (units) {
        return `${parseFloat(value).toExponential(1)} ${units}`;
    }
    else {
        const decimals = Math.max(0, -Math.floor(Math.log10(step)));
        return `${parseFloat(value).toFixed(decimals)}`;
    }
}

/**
 * Create a checkbox control row
 */
function createCheckboxGroupRow(config) {
    const row = document.createElement("div");
    row.className = "control-row";

    // Label for the group
    const groupLabel = document.createElement("label");
    groupLabel.innerHTML = config.label;
    row.appendChild(groupLabel);

    // Container for all checkboxes
    const checkboxContainer = document.createElement("div");
    checkboxContainer.className = "checkbox-group";

    config.checkboxes.forEach(checkbox => {
        const checkboxWrapper = document.createElement("span");
        checkboxWrapper.className = "checkbox-button";

        const input = document.createElement("input");
        input.type = "checkbox";
        input.name = checkbox.name;
        applyConfigAttributes(checkbox, [input], ["id", "value"]);
        input.checked = checkbox.checked || false;

        const label = document.createElement("label");
        label.setAttribute("for", checkbox.id);
        label.innerHTML = checkbox.label;

        checkboxWrapper.appendChild(input);
        checkboxWrapper.appendChild(label);
        checkboxContainer.appendChild(checkboxWrapper);
    });

    row.appendChild(checkboxContainer);

    // Apply any additional attributes
    applyConfigAttributes(config, [row, checkboxContainer], ["className"]);

    return row;
}


/**
 * Create a radio button control group row
 */
function createRadioGroupRow(config) {
    const row = document.createElement("div");
    row.className = "control-row";

    // Label for the group
    const groupLabel = document.createElement("label");
    groupLabel.innerHTML = config.label;
    row.appendChild(groupLabel);

    // Container for all radio buttons
    const radioContainer = document.createElement("div");
    radioContainer.className = "radio-group";

    config.buttons.forEach(button => {
        // Individual radio button
        const radioWrapper = document.createElement("span");
        radioWrapper.className = "radio-button";

        const input = document.createElement("input");
        input.type = "radio";
        input.name = config.name;    // ← From config
        applyConfigAttributes(button, [input], ["id", "value"]);
        input.checked = button.checked || false;

        const label = document.createElement("label");
        label.setAttribute("for", button.id);
        label.innerHTML = button.label;

        radioWrapper.appendChild(input);
        radioWrapper.appendChild(label);
        radioContainer.appendChild(radioWrapper);
    });

    row.appendChild(radioContainer);

    // Apply any additional attributes
    applyConfigAttributes(config, [groupLabel, radioContainer], ["className"]);

    return row;
}

/**
 * Helper function to apply multiple attributes from config to elements
 */
function applyConfigAttributes(config, elements, attributes) {
    attributes.forEach(attr => {
        if (config[attr] !== undefined) {
            elements.forEach(element => {
                element[attr] = config[attr];
            });
        }
    });
}

/**
 * Create a text input row
 */
function createTextInputRow(config) {
    const row = document.createElement("div");
    row.className = "control-row";

    // Label
    const label = document.createElement("label");
    label.innerHTML = config.label;
    row.appendChild(label);

    // Text input
    const input = document.createElement("input");
    input.type = "text";
    input.id = config.id;
    input.value = config.value || "";
    input.placeholder = config.placeholder || "";
    row.appendChild(input);

    // Apply any additional attributes from config to all elements
    applyConfigAttributes(config, [label, input], ["className"]);

    return row;
}

/** 
 * Convenience function to create a radio option config
 * @param {string} label - The label for the radio button
 * @param {string} id - The unique ID for the radio button element
 * @param {string} value - The value for the radio button used for control groups
 * @param {boolean} checked - Whether the radio button is checked
 * @param {string|null} className - Optional CSS class name for styling
 * @returns {Object} Radio button configuration object
*/
function radioConfig(label, id, value, checked, className = null) {
    const config = { type: "radio", label, id, value, checked };
    if (className) {
        config.className = className;
    }
    return config;
}


/**
 * Convenience function to create coordinate options radio button group
 */
function coordinatesConfig() {
    let args = ["Non-dimensional", "non-dimensional-button", "non-dimensional", true];
    const nonDimButton = radioConfig(...args);
    args = ["Dimensional", "dimensional-button", "dimensional", false];
    const dimButton = radioConfig(...args);
    return {
        type: "radio",
        label: "Coordinates:",
        name: "coordinates",
        buttons: [nonDimButton, dimButton]
    };
}

/**
 * Convenience function to create displacement toggle checkbox
 */
function overlayToggleConfig() {
    return {
        type: "checkbox",
        label: "Show:",
        checkboxes: [
            { id: "displacement-checkbox", label: "Displacement", checked: false },
            { id: "quiver-checkbox", label: "Quiver", checked: true },
            { id: "imshow-checkbox", label: "Shading", checked: true },
        ]
    };
}

/**
 * Convenience function to create imshow field selection radio button group
 */
function imshowSelectionConfig(
    fields = ["psi", "u", "v", "w", "Q", "phi"],
    labels = ["\\(\\psi\\)", "\\(u\\)", "\\(v\\)", "\\(w\\)", "\\(Q\\)", "\\(\\phi\\)"]
) {
    // Create a list of radio button configs
    const buttons = fields.map((field, index) => {
        const label = labels[index] || field;
        const id = `imshow-${field}-button`;
        const value = field;
        const checked = index === 0; // First button checked by default
        return radioConfig(label, id, value, checked);
    });

    return {
        type: "radio",
        label: "Shading:",
        name: "imshow-field",
        buttons: buttons
    };
}

/**
 * Create control row dispatcher
 */
function createControlRow(config) {
    switch (config.type) {
        case "slider":
            return createSliderRow(config);
        case "radio":
            return createRadioGroupRow(config);
        case "text":
            return createTextInputRow(config);
        case "checkbox":
            return createCheckboxGroupRow(config);
        default:
            console.warn(`Unknown control type: ${config.type}`);
            return null;
    }
}

/**
 * Create stacked model control rows based on config
 */
function createModelControls(configs, containerId = "controls") {
    const container = document.getElementById(containerId);

    // Create coordinate selection control row first
    const coordControl = coordinatesConfig();
    const coordElement = createRadioGroupRow(coordControl);
    container.appendChild(coordElement);

    // Create control rows
    configs.forEach(config => {
        const element = createControlRow(config);
        container.appendChild(element);
    });

    // Set up radio button listeners to toggle CSS classes on body
    const nonDimRadio = container.querySelector('#non-dimensional-button');
    const dimRadio = container.querySelector('#dimensional-button');

    if (nonDimRadio) nonDimRadio.addEventListener('change', () => {
        if (nonDimRadio.checked) {
            document.body.classList.remove('dimensional-mode');
            document.body.classList.add('non-dimensional-mode');
        }
    });

    if (dimRadio) dimRadio.addEventListener('change', () => {
        if (dimRadio.checked) {
            document.body.classList.remove('non-dimensional-mode');
            document.body.classList.add('dimensional-mode');
        }
    });

    // Set initial state
    document.body.classList.add('non-dimensional-mode');

    // Re-render MathJax once for all elements
    if (window.MathJax && window.MathJax.typesetPromise) {
        MathJax.typesetPromise([container]).catch(err => console.log(err));
    }
}


/** 
 * Convenience function to create a slider config object
 * @param {string} label - The label for the slider
 * @param {string} id - The unique ID for the slider element
 * @param {number} min - Minimum slider value
 * @param {number} max - Maximum slider value
 * @param {number} value - Initial slider value
 * @param {number} step - Slider step increment
 * @param {string|null} className - Optional CSS class name for styling
 * @param {string|null} units - Optional units string for display
 * @returns {Object} Slider configuration object
*/
function sliderConfig(label, id, min, max, value, step, className = null, units = null) {
    const config = { type: "slider", label, id, min, max, value, step };
    if (className !== null) {
        config.className = className;
    }
    if (units !== null) {
        config.units = units;
    }
    return config;
}

/**
 * Convenience function to apply overrides
 */
function applyOverrides(configs, overrides) {
    configs.forEach(config => {
        if (overrides[config.id]) {
            Object.assign(config, overrides[config.id]);
        }
    });
}

// Setup variables and steps to help ensure dimensional and non-dimensional sliders match up
const Omega = 2 * Math.PI / (24 * 3600); // diurnal frequency in radians per second

// const nonDimStep = 1e-2;
// const dimStep = nonDimStep * Omega;

const stepRatio = 5e-3; // Step as a ratio of the quantity's scale

const tDimMax = 4 * Math.PI / Omega; // 48 hours in seconds
const tDimStep = tDimMax * stepRatio;

const fMax = 2 * Omega;
const fValue = 0.5 * Omega;
const fDimStep = fMax * stepRatio;

const alphaMin = 1e-2 * Omega;
const alphaMax = 2 * Omega;
const alphaValue = 0.2 * Omega;
const alphaDimStep = (alphaMax - alphaMin) * stepRatio;

const NMin = 1e-1 * Omega;
const NMax = 0.1 / Omega * Omega;
const NValue = 1e-2 / Omega * Omega;
const NDimStep = (NMax - NMin) * stepRatio;

const HValue = 1e3;

/**
 * Convenience function for core dimensional coordinate control configs for gravity wave models
 */
function coreWaveConfigsDim(overrides = {}) {
    const className = "dimensional";
    const Omega = 2 * Math.PI / (24 * 3600); // diurnal freq in radians per second
    const tArgs = ["\\(t:\\)", "t_dim-slider", 0, tDimMax, 0.0, tDimStep, className, "s"];
    const fArgs = ["\\(f:\\)", "f-slider", 0, fMax, .5 * Omega, fDimStep, className, "s⁻¹"];
    const alphaArgs = ["\\(\\alpha:\\)", "alpha-slider", alphaMin, alphaMax, alphaValue, alphaDimStep, className, "s⁻¹"];
    const NArgs = ["\\(N:\\)", "N-slider", NMin, NMax, NValue, NDimStep, className, "s⁻¹"];
    // Let's leave omega out of the core controls for now, as most of the time omega = Omega
    // const omegaArgs = ["\\(\\omega:\\)", "omega-slider", 0.5 * Omega, 5 * Omega, Omega, 1e-2 * Omega, className];
    const HArgs = ["\\(H:\\)", "H-slider", 100, 5e3, HValue, 100, className, "m"];
    const Q0Args = ["\\(Q_0:\\)", "Q_0-slider", 1e-6, 10e-5, 1.2e-5, 1e-6, className, "m s⁻³"];
    const configs = [sliderConfig(...tArgs), sliderConfig(...fArgs), sliderConfig(...alphaArgs)];
    configs.push(sliderConfig(...NArgs), sliderConfig(...HArgs));
    configs.push(sliderConfig(...Q0Args));
    applyOverrides(configs, overrides);
    return configs;
}


const tNonDimMax = tDimMax * Omega; // Non-dimensional max time
const tNonDimStep = tNonDimMax * stepRatio
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
 * Convenience function for core non-dimensional config for gravity wave models
 */
function coreWaveConfigsNonDim(overrides = {}) {
    const className = "non-dimensional";
    const alOmLabel = "\\(\\alpha / \\omega :\\)";
    const NOmegaLabel = "\\(N / \\omega :\\)";
    const tArgs = ["\\(t:\\)", "t-slider", 0, tNonDimMax, 0, tNonDimStep, className];
    const fArgs = ["\\(f / \\omega :\\)", "f_omega-slider", 0, fOmMax, fOmValue, fOmNonDimStep, className];
    const alphaArgs = [alOmLabel, "alpha_omega-slider", alOmMin, alOmMax, alOmValue, alOmNonDimStep, className];
    const NArgs = [NOmegaLabel, "N_omega-slider", NOmegaMin, NOmegaMax, NOmegaValue, NOmNonDimStep, className];
    const configs = [sliderConfig(...tArgs), sliderConfig(...fArgs)];
    configs.push(sliderConfig(...alphaArgs), sliderConfig(...NArgs));
    applyOverrides(configs, overrides);
    return configs;
}

/**
 * Main function to create all wave config with coordinate toggle
 */
function coreWaveConfigs(overrides = {}) {
    return [...coreWaveConfigsNonDim(overrides), ...coreWaveConfigsDim(overrides)];
}