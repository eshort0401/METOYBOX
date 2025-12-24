containerID = "land_sea";

dimSliders = coreWaveSlidersDim(containerID);
nonDimSliders = coreWaveSlidersNonDim(containerID);

// Change starting values of t and alpha sliders
dimSliders.tSlider.value = Math.PI / 2;
dimSliders.alphaOmegaSlider.value = 0.1;

// Add new sliders for L
const LStep = 1 * stepRatio;
const LValue = 0.1;
const LDimValue = (LValue * NValue * HValue) / Omega;
nonDimSliders.LSlider = createSliderRow(
    `${containerID}-L-slider`,
    `${containerID}-L-output`,
    "\\(L:\\)",
    LStep,
    1,
    LValue,
    LStep,
    "non-dimensional"
);
dimSliders.LDimSlider = createSliderRow(
    `${containerID}-L_dim-slider`,
    `${containerID}-L_dim-output`,
    "\\(L:\\)",
    LStep * 100e3,
    100e3,
    LDimValue,
    LStep * 100e3,
    "dimensional",
    "m"
);

coordinateToggle = createCoordinateSelectionRow(containerID);
overlayToggle = createOverlayToggleRow(containerID);
imshowSelection = createImshowSelectionRow(
    containerID,
    ["psi", "u", "v", "w", "Q"],
    ["\\(\\psi\\)", "\\(u\\)", "\\(v\\)", "\\(w\\)", "\\(Q\\)"]
);

// Get the relevant div container
container = document.getElementById(`${containerID} #main-content #controls`);
// Append all the control rows to the container
container.append(coordinateToggle, overlayToggle, imshowSelection);
container.append(...Object.values(nonDimSliders), ...Object.values(dimSliders));
setupCoordinateToggle(containerID);
