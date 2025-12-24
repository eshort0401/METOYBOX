/**
 * Create a slider row. Note the ids should be unique across the document.
 * @param {string} input_id - id for the input element; must be unique across document
 * @param {string} output_id - id for the output element; must be unique across document
 * @param {string} label_text - label text
 * @param {number} min - Min slider value
 * @param {number} max - Max slider value
 * @param {number} value - Initial value
 * @param {number} step - Slider step
 * @param {string|null} className - Optional CSS class
 * @param {string|null} units - Optional units for display
 */
function createSliderRow(
    input_id,
    output_id,
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
    Object.assign(input, { type: "range", min, max, step, value, input_id });

    // Output
    const output = document.createElement("output");
    output.id = output_id;
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
function createCheckbox(id, label_text, name, checked, value) {
    // Create a wrapper for each individual textbox to hold the box and label
    const checkboxWrapper = document.createElement("span");
    checkboxWrapper.className = "checkbox-button";

    const input = document.createElement("input");
    // Give the id to the input element; thats the thing we care about for controlling our models
    Object.assign(input, { type: "checkbox", value, id, name });
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
function createRadioButton(id, label_text, name, checked) {
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
 * Helper function to apply multiple attributes from config to elements
 */
// function applyAttributes(config, elements, attributes) {
//     attributes.forEach((attr) => {
//         if (config[attr] !== undefined) {
//             elements.forEach((element) => {
//                 element[attr] = config[attr];
//             });
//         }
//     });
// }

/**
 * Create a text input row
 */
// function createTextInputRow(config) {
//     const row = document.createElement("div");
//     row.className = "control-row";

//     // Label
//     const label = document.createElement("label");
//     label.innerHTML = config.label;
//     row.appendChild(label);

//     // Text input
//     const input = document.createElement("input");
//     input.type = "text";
//     input.id = config.id;
//     input.value = config.value || "";
//     input.placeholder = config.placeholder || "";
//     row.appendChild(input);

//     // Apply any additional attributes from config to all elements
//     applyAttributes(config, [label, input], ["className"]);

//     return row;
// }

/**
 * Convenience function to create a radio option config
 * @param {string} label - The label for the radio button
 * @param {string} id - The unique ID for the radio button element
 * @param {string} value - The value for the radio button used for control groups
 * @param {boolean} checked - Whether the radio button is checked
 * @param {string|null} className - Optional CSS class name for styling
 * @returns {Object} Radio button configuration object
 */
// function radioConfig(label, id, value, checked, className = null) {
//     const config = { type: "radio", label, id, value, checked };
//     if (className) {
//         config.className = className;
//     }
//     return config;
// }

/**
 * Convenience function to create coordinate options radio button group
 */
// function coordinatesConfig(starting_coordinates = "non-dimensional") {
//     let args = [
//         "Non-dimensional",
//         "non-dimensional-button",
//         "non-dimensional",
//         starting_coordinates === "non-dimensional",
//     ];
//     const nonDimButton = radioConfig(...args);
//     args = [
//         "Dimensional",
//         "dimensional-button",
//         "dimensional",
//         starting_coordinates === "dimensional",
//     ];
//     const dimButton = radioConfig(...args);
//     return {
//         type: "radio",
//         label: "Coordinates:",
//         name: "coordinates",
//         buttons: [nonDimButton, dimButton],
//     };
// }

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
        starting_coordinates === "non-dimensional"
    );
    const dimButton = createRadioButton(
        `${container_id}-dimensional-button`,
        "Dimensional",
        `${container_id}-coordinates`,
        starting_coordinates === "dimensional"
    );
    return createRadioGroupRow("Coordinates:", [nonDimButton, dimButton]);
}

/**
 * Convenience function to create overlay toggle checkbox
 */
// function overlayToggleConfig() {
//     return {
//         type: "checkbox",
//         label: "Show:",
//         checkboxes: [
//             {
//                 id: "displacement-checkbox",
//                 label: "Displacement",
//                 checked: false,
//             },
//             { id: "quiver-checkbox", label: "Quiver", checked: true },
//             { id: "imshow-checkbox", label: "Shading", checked: true },
//         ],
//     };
// }

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
            `${container_id}-imshow`,
            index === 0 // First button checked by default
        );
    });

    return createRadioGroupRow("Shading:", buttons);
}

/**
 * Create control row dispatcher
 */
// function createControlRow(config) {
//     switch (config.type) {
//         case "slider":
//             return createSliderRow(config);
//         case "radio":
//             return createRadioGroupRow(config);
//         case "text":
//             return createTextInputRow(config);
//         case "checkbox":
//             return createCheckboxGroupRow(config);
//         default:
//             console.warn(`Unknown control type: ${config.type}`);
//             return null;
//     }
// }

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
// function sliderConfig(
//     label,
//     id,
//     min,
//     max,
//     value,
//     step,
//     className = null,
//     units = null
// ) {
//     const config = { type: "slider", label, id, min, max, value, step };
//     if (className !== null) {
//         config.className = className;
//     }
//     if (units !== null) {
//         config.units = units;
//     }
//     return config;
// }

/**
 * Convenience function to apply overrides
 */
// function applyOverrides(configs, overrides) {
//     configs.forEach((config) => {
//         if (overrides[config.id]) {
//             Object.assign(config, overrides[config.id]);
//         }
//     });
// }

// Setup variables and steps to help ensure dimensional and non-dimensional sliders match up
const Omega = (2 * Math.PI) / (24 * 3600); // diurnal frequency in radians per second

// const nonDimStep = 1e-2;
// const dimStep = nonDimStep * Omega;

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

/**
 * Convenience function for core dimensional coordinate control configs for gravity wave models
 */
// function coreWaveConfigsDim(overrides = {}) {
//     const className = "dimensional";
//     const Omega = (2 * Math.PI) / (24 * 3600); // diurnal freq in radians per second
//     const tArgs = [
//         "\\(t:\\)",
//         "t_dim-slider",
//         0,
//         tDimMax,
//         0.0,
//         tDimStep,
//         className,
//         "s",
//     ];
//     const fArgs = [
//         "\\(f:\\)",
//         "f-slider",
//         0,
//         fMax,
//         0.5 * Omega,
//         fDimStep,
//         className,
//         "s⁻¹",
//     ];
//     const alphaArgs = [
//         "\\(\\alpha:\\)",
//         "alpha-slider",
//         alphaMin,
//         alphaMax,
//         alphaValue,
//         alphaDimStep,
//         className,
//         "s⁻¹",
//     ];
//     const NArgs = [
//         "\\(N:\\)",
//         "N-slider",
//         NMin,
//         NMax,
//         NValue,
//         NDimStep,
//         className,
//         "s⁻¹",
//     ];
//     // Let's leave omega out of the core controls for now, as most of the time omega = Omega
//     // const omegaArgs = ["\\(\\omega:\\)", "omega-slider", 0.5 * Omega, 5 * Omega, Omega, 1e-2 * Omega, className];
//     const HArgs = [
//         "\\(H:\\)",
//         "H-slider",
//         100,
//         5e3,
//         HValue,
//         100,
//         className,
//         "m",
//     ];
//     const Q0Args = [
//         "\\(Q_0:\\)",
//         "Q_0-slider",
//         1e-6,
//         10e-5,
//         1.2e-5,
//         1e-6,
//         className,
//         "m s⁻³",
//     ];
//     const configs = [
//         sliderConfig(...tArgs),
//         sliderConfig(...fArgs),
//         sliderConfig(...alphaArgs),
//     ];
//     configs.push(
//         sliderConfig(...NArgs),
//         sliderConfig(...Q0Args),
//         sliderConfig(...HArgs)
//     );
//     applyOverrides(configs, overrides);
//     return configs;
// }

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
 * Convenience function for core non-dimensional config for gravity wave models
 */
// function coreWaveConfigsNonDim(overrides = {}) {
//     const className = "non-dimensional";
//     const alOmLabel = "\\(\\alpha / \\omega :\\)";
//     const NOmegaLabel = "\\(N / \\omega :\\)";
//     const tArgs = [
//         "\\(t:\\)",
//         "t-slider",
//         0,
//         tNonDimMax,
//         0,
//         tNonDimStep,
//         className,
//     ];
//     const fArgs = [
//         "\\(f / \\omega :\\)",
//         "f_omega-slider",
//         0,
//         fOmMax,
//         fOmValue,
//         fOmNonDimStep,
//         className,
//     ];
//     const alphaArgs = [
//         alOmLabel,
//         "alpha_omega-slider",
//         alOmMin,
//         alOmMax,
//         alOmValue,
//         alOmNonDimStep,
//         className,
//     ];
//     const NArgs = [
//         NOmegaLabel,
//         "N_omega-slider",
//         NOmegaMin,
//         NOmegaMax,
//         NOmegaValue,
//         NOmNonDimStep,
//         className,
//     ];
//     const configs = [sliderConfig(...tArgs), sliderConfig(...fArgs)];
//     configs.push(sliderConfig(...alphaArgs), sliderConfig(...NArgs));
//     applyOverrides(configs, overrides);
//     return configs;
// }

/**
 * Main function to create all wave config with coordinate toggle
 */
function coreWaveConfigs(overrides = {}) {
    return [
        ...coreWaveConfigsNonDim(overrides),
        ...coreWaveConfigsDim(overrides),
    ];
}
