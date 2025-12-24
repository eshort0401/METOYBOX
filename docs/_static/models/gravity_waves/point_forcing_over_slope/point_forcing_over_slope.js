const configs = coreWaveConfigs();
// Add a displacement toggle checkbox row above the sliders
const displacement_config = overlayToggleConfig();
configs.unshift(displacement_config);

// Add an imshow selection control row above the sliders
const fields = ["psi", "u", "v", "w", "phi"]
const labels = ["\\(\\psi\\)", "\\(u\\)", "\\(v\\)", "\\(w\\)", "\\(\\phi\\)"]
const imshow_sel_config = imshowSelectionConfig(fields, labels);
configs.unshift(imshow_sel_config);
const MStep = 3 * stepRatio
const MDimMax = 1e-2
const MDimStep = MDimMax * stepRatio
const zFStep = 3 * stepRatio
let args = ["\\(M:\\)", "M-slider", 0, 3, 0.2, MStep, "non-dimensional"];
configs.push(sliderConfig(...args));
args = ["\\(z_f:\\)", "z_f-slider", 0, 3, 1, zFStep, "non-dimensional"];
configs.push(sliderConfig(...args));
args = ["\\(z_f:\\)", "z_f_dim-slider", 0, 3e3, 1e3, zFStep * 1e3, "dimensional", "m"];
configs.push(sliderConfig(...args));
args = ["\\(M:\\)", "M_dim-slider", 0, MDimMax, Omega * 1e2, MDimStep, "dimensional", "m m⁻¹"];
configs.push(sliderConfig(...args));
args = ["\\(\\omega:\\)", "omega-slider", Omega * stepRatio, 2 * Omega, Omega, Omega * stepRatio, "dimensional", "s⁻¹"];
configs.push(sliderConfig(...args));
createModelControls(configs, "controls");
