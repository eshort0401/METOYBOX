// Note containerID is set by utils.py

const dimSliders = coreWaveSlidersDim(containerID);
const nonDimSliders = coreWaveSlidersNonDim(containerID);

// Add new sliders for M, z_f and omega
nonDimSliders.MNonDimSlider = getMNonDimSlider(containerID);
dimSliders.MDimSlider = getMDimSlider(containerID);

const coordinateToggle = createCoordinateSelectionRow(containerID);
const overlayToggle = createOverlayToggleRow(containerID);
const imshowSelection = createFieldSelectionRow(
    containerID,
    ["psi", "u", "v", "w", "phi", "Q"],
    ["\\(\\psi\\)", "\\(u\\)", "\\(v\\)", "\\(w\\)", "\\(\\phi\\)", "\\(Q\\)"]
);

// Get the relevant div container
container = document.querySelector(`#${containerID} #main-content #controls`);
// Append all the control rows to the container
container.append(coordinateToggle, overlayToggle, imshowSelection);
container.append(...Object.values(nonDimSliders), ...Object.values(dimSliders));
setupCoordinateToggle(containerID);