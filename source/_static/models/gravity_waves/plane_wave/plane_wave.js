// Note containerID is set by utils.py

const dimSliders = coreWaveSlidersDim(containerID);
delete dimSliders.Q0Slider;
const nonDimSliders = coreWaveSlidersNonDim(containerID);

// Allow alpha to be zero for these models (also initialize to zero)
nonDimSliders.alphaOmegaSlider.querySelector('input').min = 0;
dimSliders.alphaSlider.querySelector('input').min = 0;
nonDimSliders.alphaOmegaSlider.querySelector('input').value = 0;
dimSliders.alphaSlider.querySelector('input').value = 0;

// Add sliders for k and sigma
nonDimSliders.kNonDimSlider = getKNonDimSlider(containerID);
dimSliders.kDimSlider = getKDimSlider(containerID);

nonDimSliders.sigmaNonDimSlider = getSigmaNonDimSlider(containerID);
dimSliders.sigmaDimSlider = getSigmaDimSlider(containerID);

const coordinateToggle = createCoordinateSelectionRow(containerID);
const overlayToggle = createOverlayToggleRow(containerID);
const imshowSelection = createImshowSelectionRow(
    containerID,
    ["psi", "u", "v", "w", "phi"],
    ["\\(\\psi\\)", "\\(u\\)", "\\(v\\)", "\\(w\\)", "\\(\\phi\\)"]
);

// Get the relevant div container
container = document.querySelector(`#${containerID} #main-content #controls`);
// Append all the control rows to the container
container.append(coordinateToggle, overlayToggle, imshowSelection);
container.append(...Object.values(nonDimSliders), ...Object.values(dimSliders));
setupCoordinateToggle(containerID);
