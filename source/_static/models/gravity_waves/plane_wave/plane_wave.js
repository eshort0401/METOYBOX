// Note containerID is set by utils.py

const dimSliders = coreWaveSlidersDim(containerID);
delete dimSliders.Q0Slider;
const nonDimSliders = coreWaveSlidersNonDim(containerID);

// Allow alpha to be zero for these models (also initialize to zero)
nonDimSliders.alphaOmegaSlider.querySelector("input").min = 0;
dimSliders.alphaSlider.querySelector("input").min = 0;
nonDimSliders.alphaOmegaSlider.querySelector("input").value = 0;
dimSliders.alphaSlider.querySelector("input").value = 0;

// Add sliders for k and sigma
nonDimSliders.kNonDimSlider = getKNonDimSlider(containerID);
dimSliders.kDimSlider = getKDimSlider(containerID);

nonDimSliders.sigmaNonDimSlider = getSigmaNonDimSlider(containerID);
dimSliders.sigmaDimSlider = getSigmaDimSlider(containerID);

const coordinateToggle = createCoordinateSelectionRow(containerID);
const overlayToggle = createOverlayToggleRow(containerID);
const imshowSelection = createFieldSelectionRow(
    containerID,
    ["psi", "u", "v", "w", "phi"],
    ["\\(\\psi\\)", "\\(u\\)", "\\(v\\)", "\\(w\\)", "\\(\\phi\\)"]
);
// TODO: Implement multiple quiver options
// const quiverSelection = createFieldSelectionRow(
//     containerID,
//     ["velocity", "acceleration", "buoyancy", "coriolis", "grad_phi"],
//     [
//         "\\( \\mathbf{u} \\)",
//         "\\( \\frac{\\partial}{\\partial t} \\mathbf{u} \\)",
//         "\\(b\\mathbf{k} \\)",
//         "\\( \\mathbf{u} \\times f\\mathbf{k} \\)",
//         "\\( - \\nabla \\phi \\)",
//     ],
//     "quiver"
// );
const quiverSelection = createFieldSelectionRow(
    containerID,
    ["velocity", "grad_phi"],
    [
        "\\( \\mathbf{u} \\)",
        "\\( - \\nabla \\phi \\)",
    ],
    "quiver"
);

// Get the relevant div container
container = document.querySelector(`#${containerID} #main-content #controls`);
// Append all the control rows to the container
container.append(
    coordinateToggle,
    overlayToggle,
    imshowSelection,
    quiverSelection
);
container.append(...Object.values(nonDimSliders), ...Object.values(dimSliders));
setupCoordinateToggle(containerID);
