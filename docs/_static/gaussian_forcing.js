const configs = coreWaveConfigs();
// Add a displacement toggle checkbox row above the sliders
const displacement_config = overlayToggleConfig();
configs.unshift(displacement_config);

// Add an imshow selection control row above the sliders
const fields = ["psi", "u", "v", "w", "phi"]
const labels = ["\\(\\psi\\)", "\\(u\\)", "\\(v\\)", "\\(w\\)", "\\(\\phi\\)"]
const imshow_sel_config = imshowSelectionConfig(fields, labels);
configs.unshift(imshow_sel_config);
const zFStep = 3 * stepRatio
const LStep = 1 * stepRatio
const LValue = 0.2
const LDimValue = LValue * NValue * HValue / Omega
args = ["\\(z_f:\\)", "z_f-slider", 0, 3, 1, zFStep, "non-dimensional"];
configs.push(sliderConfig(...args));
args = ["\\(z_f:\\)", "z_f_dim-slider", 0, 3e3, 1e3, zFStep * 1e3, "dimensional", "m"];
configs.push(sliderConfig(...args));
args = ["\\(\\omega:\\)", "omega-slider", Omega * stepRatio, 2 * Omega, Omega, Omega * stepRatio, "dimensional", "s⁻¹"];
configs.push(sliderConfig(...args));
const sigmaMin = 0.1
const sigmaMax = 5
const sigmaStep = (sigmaMax - sigmaMin) * stepRatio
const sigmaDimMin = sigmaMin * Omega
const sigmaDimMax = sigmaMax * Omega
const sigmaDimStep = sigmaStep * Omega
args = ["\\(\\sigma:\\)", "sigma-slider", sigmaMin, sigmaMax, 1, sigmaStep, "non-dimensional"];
configs.push(sliderConfig(...args));
args = ["\\(\\sigma:\\)", "sigma_dim-slider", sigmaDimMin, sigmaDimMax, Omega, sigmaDimStep, "dimensional", "s⁻¹"];
configs.push(sliderConfig(...args));
createModelControls(configs, "controls");
