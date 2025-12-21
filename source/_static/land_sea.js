const configs = coreWaveConfigs();
// Change the default starting value of the t slider
configs[0].value = Math.PI / 2;
// Change the default starting value of alpha
configs[2].value = 0.1;
// Add a displacement toggle checkbox row above the sliders
const overlay_toggle_config = overlayToggleConfig();
configs.unshift(overlay_toggle_config);

// Add an imshow selection control row above the sliders
const fields = ["psi", "u", "v", "w", "Q"]
const labels = ["\\(\\psi\\)", "\\(u\\)", "\\(v\\)", "\\(w\\)", "\\(Q\\)"]
configs.unshift(imshowSelectionConfig(fields, labels));
const LStep = 1 * stepRatio
const LValue = 0.1
const LDimValue = LValue * NValue * HValue / Omega
args = ["\\(L:\\)", "L-slider", LStep, 1, LValue, LStep, "non-dimensional"];
configs.push(sliderConfig(...args));
args = ["\\(L:\\)", "L_dim-slider", LStep * 100e3, 100e3, LDimValue, LStep * 100e3, "dimensional", "m"];
configs.push(sliderConfig(...args));
createModelControls(configs, "controls");