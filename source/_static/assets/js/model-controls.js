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
        input.value = slider.value;
        input.step = slider.step;
        row.appendChild(input);

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