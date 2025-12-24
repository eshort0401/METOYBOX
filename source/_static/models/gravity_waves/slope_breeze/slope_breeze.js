const configs = coreWaveConfigs();
// Add a displacement toggle checkbox row above the sliders
const displacement_config = overlayToggleConfig();
configs.unshift(displacement_config);

// Add an imshow selection control row above the sliders
const imshow_sel_config = imshowSelectionConfig();
configs.unshift(imshow_sel_config);
const MStep = 3 * stepRatio
const MDimMax = 1e-2
const MDimStep = MDimMax * stepRatio
let args = ["\\(M:\\)", "M-slider", 0, 3, 0.2, MStep, "non-dimensional"];
configs.push(sliderConfig(...args));
args = ["\\(M:\\)", "M_dim-slider", 0, MDimMax, Omega * 1e2, MDimStep]
args.push("dimensional", "m m⁻¹");
configs.push(sliderConfig(...args));
createModelControls(configs, "controls");