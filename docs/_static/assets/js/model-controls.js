/**
 * Create a slider row
 */
function createSliderRow(config) {
    const row = document.createElement("div");
    row.classList.add("control-row");
    row.classList.add(config.className);     // Add "dimensional" or "non-dimensional"

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
    output.textContent = config.value;
    row.appendChild(output);

    // Update output on slider change
    input.addEventListener("input", () => {
        output.textContent = input.value;
    });

    // Apply any additional attributes from config to all elements
    applyConfigAttributes(config, [label, input, output], ["className"]);

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
function createTextInputControl(config) {
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
function createCoordinateControl() {
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
 * Create stacked model control rows based on config
 */
function createModelControls(controls, containerId = "controls") {
    const container = document.getElementById(containerId);

    // Create radio buttons first
    const coordControl = createCoordinateControl();
    const coordElement = createRadioGroupRow(coordControl);
    container.appendChild(coordElement);

    // Create ALL sliders (both dimensional and non-dimensional) 
    controls.forEach(config => {
        const element = createSliderRow(config);
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
 * @returns {Object} Slider configuration object
*/
function sliderConfig(label, id, min, max, value, step, className = null) {
    const config = { type: "slider", label, id, min, max, value, step };
    if (className) {
        config.className = className;
    }
    return config;
}

/**
 * Convenience function to apply overrides
 */
function applyOverrides(controls, overrides) {
    controls.forEach(ctrl => {
        if (overrides[ctrl.id]) {
            Object.assign(ctrl, overrides[ctrl.id]);
        }
    });
}

/**
 * Convenience function for core non-dimensional controls for gravity wave models
 */
function coreWaveControlsNonDim(overrides = {}) {
    const className = "non-dimensional";
    const tArgs = ["\\(t:\\)", "t-slider", 0, 12.56637, 0.0, 0.01, className];
    const fArgs = ["\\(f / \\omega :\\)", "f-omega-slider", 0, 2, 0.51, 0.01, className];
    const alphaArgs = ["\\(\\alpha / \\omega :\\)", "alpha-omega-slider", 0.01, 1, 0.2, 0.01, className];
    const NArgs = ["\\(N / \\omega :\\)", "N-omega-slider", 0.1, 150, 137.5, 0.1, className];
    const controls = [sliderConfig(...tArgs), sliderConfig(...fArgs)];
    controls.push(sliderConfig(...alphaArgs), sliderConfig(...NArgs));
    applyOverrides(controls, overrides);
    return controls;
}


/**
 * Convenience function for core dimensional controls for gravity wave models
 */
function coreWaveControlsDim(overrides = {}) {
    const className = "dimensional";
    const tArgs = ["\\(t:\\)", "t-dim-slider", 0, 12.56637, 0.0, 0.01, className];
    const fArgs = ["\\(f:\\)", "f-slider", 0, 2, 0.51, 0.01, className];
    const alphaArgs = ["\\(\\alpha:\\)", "alpha-slider", 0.01, 1, 0.2, 0.01, className];
    const NArgs = ["\\(N:\\)", "N-slider", 0.1, 150, 137.5, 0.1, className];
    const omegaArgs = ["\\(\\omega:\\)", "omega-slider", 0.0001, 0.01, 0.00174, 0.0001, className];
    const controls = [sliderConfig(...tArgs), sliderConfig(...fArgs), sliderConfig(...alphaArgs)];
    controls.push(sliderConfig(...NArgs), sliderConfig(...omegaArgs));
    applyOverrides(controls, overrides);
    return controls;
}

/**
 * Main function to create all wave controls with coordinate toggle
 */
function coreWaveControls(overrides = {}) {
    return [...coreWaveControlsNonDim(overrides), ...coreWaveControlsDim(overrides)];
}