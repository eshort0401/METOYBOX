function createModelControls(config, containerId = "controls") {
    const container = document.getElementById(containerId);

    config.forEach(slider => {
        // Row wrapper
        const row = document.createElement("div");
        row.className = "slider-row";

        // Label
        const label = document.createElement("label");
        label.innerHTML = slider.label;
        row.appendChild(label);

        // Slider
        const input = document.createElement("input");
        input.type = "range";
        input.id = slider.id;
        input.min = slider.min;
        input.max = slider.max;
        input.step = slider.step;
        row.appendChild(input);

        // Set initial value
        input.value = slider.value;

        // Output
        const output = document.createElement("output");
        output.id = slider.id.replace("_slider", "_out");
        output.textContent = slider.value;
        row.appendChild(output);

        container.appendChild(row);

        // Update output on slider change
        input.addEventListener("input", () => {
            output.textContent = input.value;
        });
    });
}

function coreWaveControls(overrides = {}) {
    // Default core sliders that appear in most models
    const controls = [
        { label: "\\(t:\\)", id: 't_slider', min: 0, max: 12.56637, value: 0.0, step: 0.01 },
        { label: "\\(f / \\omega :\\)", id: 'f_omega_slider', min: 0, max: 2, value: 0.51, step: 0.01 },
        { label: "\\(\\alpha / \\omega :\\)", id: 'alpha_omega_slider', min: 0.01, max: 1, value: 0.2, step: 0.01 },
        { label: "\\(N / \\omega :\\)", id: 'N_omega_slider', min: 0.1, max: 150, value: 137.5, step: 0.1 },
    ];

    // Apply any overrides (e.g., different default values)
    controls.forEach(ctrl => {
        if (overrides[ctrl.id]) {
            Object.assign(ctrl, overrides[ctrl.id]);
        }
    });

    return controls;
}
