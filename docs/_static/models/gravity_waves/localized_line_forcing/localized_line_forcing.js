// Note containerID is set by utils.py

const dimSliders = coreWaveSlidersDim(containerID);
const nonDimSliders = coreWaveSlidersNonDim(containerID);

// Add new sliders for L, z_f and omega
nonDimSliders.LSlider = getLNonDimSlider(containerID);
dimSliders.LDimSlider = getLDimSlider(containerID);

nonDimSliders.zFSlider = getZfNonDimSlider(containerID);
dimSliders.zFDimSlider = getZfDimSlider(containerID);

dimSliders.omegaSlider = getOmegaSlider(containerID);

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