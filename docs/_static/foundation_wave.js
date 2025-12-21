const configs = coreWaveConfigs();
// Add a displacement toggle checkbox row above the sliders
const displacement_config = overlayToggleConfig();
configs.unshift(displacement_config);

// Add an imshow selection control row above the sliders
const fields = ["psi", "u", "v", "w", "phi"]
const labels = ["\\(\\psi\\)", "\\(u\\)", "\\(v\\)", "\\(w\\)", "\\(\\phi\\)"]
const imshow_sel_config = imshowSelectionConfig(fields, labels);
configs.unshift(imshow_sel_config);

const kMin = 0.1
const kMax = 5
const kStep = (kMax - kMin) * stepRatio
const kValue = 2 * Math.PI // Set starting horizontal wavelength to 1 non-dimensional unit
let args = ["\\(k:\\)", "k-slider", kMin, kMax, kValue, kStep, "non-dimensional"];
configs.push(sliderConfig(...args));

const scale = Omega / (NValue * HValue)
const kMinDim = kMin * scale
const kMaxDim = kMax * scale
const kStepDim = kStep * scale
args = ["\\(k:\\)", "k_dim-slider", kMinDim, kMaxDim, kValue * scale, kStepDim, "dimensional"];
configs.push(sliderConfig(...args));

const sigmaMin = 0.1
const sigmaMax = 5
const sigmaStep = (sigmaMax - sigmaMin) * stepRatio
args = ["\\(\\sigma:\\)", "sigma-slider", sigmaMin, sigmaMax, 1, sigmaStep, "non-dimensional"];
configs.push(sliderConfig(...args));
const sigmaMinDim = sigmaMin * Omega
const sigmaMaxDim = sigmaMax * Omega
const sigmaStepDim = sigmaStep * Omega
args = ["\\(\\sigma:\\)", "sigma_dim-slider", sigmaMinDim, sigmaMaxDim, Omega, sigmaStepDim, "dimensional"];
configs.push(sliderConfig(...args));
createModelControls(configs, "controls");