// Note containerID is set by utils.py

const dimSliders = coreWaveSlidersDim(containerID);
const nonDimSliders = coreWaveSlidersNonDim(containerID);

// Add new sliders for L
nonDimSliders.LSlider = getLNonDimSlider(containerID);
dimSliders.LDimSlider = getLDimSlider(containerID);

startingCoords = "dimensional";
const coordToggle = createCoordinateSelectionRow(containerID, startingCoords);
const overlayToggle = createOverlayToggleRow(containerID);
// Note we switch off the quiver by default for the intro figure
overlayToggle.querySelector(`#${containerID}-quiver-checkbox`).checked = false;
// Note we change the default variable order for the intro figure to highlight Q
const imshowSelection = createFieldSelectionRow(
    containerID,
    ["Q", "psi", "u", "v", "w"],
    ["\\(Q\\)", "\\(\\psi\\)", "\\(u\\)", "\\(v\\)", "\\(w\\)"]
);

// Get the relevant div container
container = document.querySelector(`#${containerID} #main-content #controls`);
// Append all the control rows to the container
container.append(coordToggle, overlayToggle, imshowSelection);
container.append(...Object.values(nonDimSliders), ...Object.values(dimSliders));
setupCoordinateToggle(containerID, startingCoords);
