// Note containerID is set by utils.py

const dimSliders = coreWaveSlidersDim(containerID);
const nonDimSliders = coreWaveSlidersNonDim(containerID);

// Change starting values of t and alpha sliders
// Remember the "input" objects here are the sliders themselves.
nonDimSliders.tSlider.querySelector('input').value = Math.PI / 2;
nonDimSliders.alphaOmegaSlider.querySelector('input').value = 0.1;

// Add new sliders for L
nonDimSliders.LNonDimSlider = getLNonDimSlider(containerID);
dimSliders.LDimSlider = getLDimSlider(containerID);

const coordinateToggle = createCoordinateSelectionRow(containerID);
const overlayToggle = createOverlayToggleRow(containerID);
const imshowSelection = createFieldSelectionRow(
    containerID,
    ["psi", "u", "v", "w", "Q"],
    ["\\(\\psi\\)", "\\(u\\)", "\\(v\\)", "\\(w\\)", "\\(Q\\)"]
);

// Get the relevant div container
const container = document.querySelector(`#${containerID} #main-content #controls`);
// Append all the control rows to the container
container.append(coordinateToggle, overlayToggle, imshowSelection);
container.append(...Object.values(nonDimSliders), ...Object.values(dimSliders));
setupCoordinateToggle(containerID);
