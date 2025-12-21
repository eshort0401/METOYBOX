// Override the default slider configuration
const overrides = {
    "t-slider": { value: 2.0 },
    "f-omega-slider": { value: 0.7 },
    "alpha-omega-slider": { value: 0.1 },
};
const configs = coreWaveConfigs(overrides);
createModelControls(configs, "controls");