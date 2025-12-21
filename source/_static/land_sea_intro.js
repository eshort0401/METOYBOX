const configs = coreWaveConfigs();

// Add a displacement toggle checkbox row above the sliders
const overlay_toggle_config = overlayToggleConfig();
// Switch off the quiver upon loading
overlay_toggle_config.checkboxes[1].checked = false;
configs.unshift(overlay_toggle_config);

// Add an imshow selection control row above the sliders
const fields = ["Q", "psi", "u", "v", "w"]
const labels = ["\\(Q\\)", "\\(\\psi\\)", "\\(u\\)", "\\(v\\)", "\\(w\\)"]
imshow_selection_config = imshowSelectionConfig(fields, labels);

configs.unshift(imshow_selection_config);
const LStep = 1 * stepRatio
const LValue = 0.2
const LDimValue = LValue * NValue * HValue / Omega
args = ["\\(L:\\)", "L-slider", LStep, 1, LValue, LStep, "non-dimensional"];
configs.push(sliderConfig(...args));
args = ["\\(L:\\)", "L_dim-slider", LStep * 100e3, 100e3, LDimValue, LStep * 100e3, "dimensional", "m"];
configs.push(sliderConfig(...args));
createModelControls(configs, "controls", "dimensional");