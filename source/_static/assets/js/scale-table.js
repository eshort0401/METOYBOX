class ScaleTable {
    /**
     * Initialize a ScaleTable instance
     * @param {string} containerID - The container element id
     * @param {string[][]} labels - Array of term labels
     * @param {string[][]} values - Array of corresponding values
     * @param {string[]} units - Array of units for each equation
     * @param {string[]} inferredScaleLabels - Array of inferred scale labels
     * @param {string[]} inferredScaleValues - Array of inferred scale values
     * @param {string} name - Optional name for the table so can ensure unique IDs
     */
    constructor(
        containerID,
        labels,
        values,
        units,
        inferredScaleLabels,
        inferredScaleValues,
        name = "scale-table"
    ) {
        this.id = `${containerID}-${name}`;
        // Build row and column ids programmatically
        this.ids = labels.map((row, i) =>
            row.map((term, j) => `${this.id}-${i}-${j}`)
        );
        this.inferredScaleIDs = inferredScaleLabels.map(
            (label, i) => `${this.id}-inferred-scale-${i}`
        );

        this.labels = labels;
        this.values = values;
        this.units = units;
        this.inferredScaleLabels = inferredScaleLabels;
        this.inferredScaleValues = inferredScaleValues;

        // Build the inferred scales div
        const inferredScalesDiv = document.createElement("span");
        inferredScalesDiv.id = `${containerID}-${name}-inferred-scales`;
        for (let i = 0; i < inferredScaleLabels.length; i++) {
            const labelSpan = document.createElement("span");
            labelSpan.innerHTML = `\\(${inferredScaleLabels[i]}\\) = `;
            const valueSpan = document.createElement("span");
            valueSpan.id = this.inferredScaleIDs[i];
            const value = this.inferredScaleValues[i];
            this._updateValue(valueSpan, value);
            inferredScalesDiv.append(labelSpan, valueSpan);
            if (i < inferredScaleLabels.length - 1) {
                inferredScalesDiv.append(document.createTextNode(", "));
            }
        }

        // Build the table itself
        const table = document.createElement("table");
        const tbody = document.createElement("tbody");
        for (let i = 0; i < labels.length; i++) {
            const label_tr = document.createElement("tr");
            const value_tr = document.createElement("tr");
            // Add a css class to create rulers between equations (skip last)
            if (i < labels.length - 1) {
                value_tr.classList.add("ruler-bottom");
            }
            for (let j = 0; j < labels[i].length; j++) {
                const label_td = document.createElement("td");
                const value_td = document.createElement("td");
                // Set the value td to have the id for updating later
                value_td.id = this.ids[i][j];
                // Initialize the table label
                const term = this.labels[i][j];
                label_td.innerHTML = `\\(${term}\\)`;
                // Initialize the table value
                this._updateTableValue(value_td, i, j);
                label_tr.appendChild(label_td);
                value_tr.appendChild(value_td);
            }
            tbody.append(label_tr, value_tr);

            const unit_label_td = document.createElement("td");
            const unit_value_td = document.createElement("td");
            unit_label_td.innerHTML = "unit";
            unit_value_td.innerHTML = this.units[i];
            unit_label_td.classList.add("ruler-left");
            unit_value_td.classList.add("ruler-left");
            label_tr.appendChild(unit_label_td);
            value_tr.appendChild(unit_value_td);
        }

        table.appendChild(tbody);
        this.table = table;
        this.inferredScalesDiv = inferredScalesDiv;
    }

    /**
     * Update the scale table in the DOM with new values. Assumes the table
     * has already been created and added to the DOM.
     */
    update() {
        // Update the table values
        for (let i = 0; i < this.ids.length; i++) {
            for (let j = 0; j < this.ids[i].length; j++) {
                const value_td = document.getElementById(this.ids[i][j]);
                this._updateTableValue(value_td, i, j);
            }
        }
        // Update the inferred scales
        for (let i = 0; i < this.inferredScaleIDs.length; i++) {
            const value = this.inferredScaleValues[i];
            const value_td = document.getElementById(this.inferredScaleIDs[i]);
            const exponent = Math.log10(Math.abs(value)).toFixed(1);
            value_td.innerHTML = `10<sup>${exponent}</sup>`;
        }
    }

    /**
     * Convenience method to update a single table value
     * @param {HTMLElement} td - The table cell to update
     * @param {number} i - The row index
     * @param {number} j - The column index
     */
    _updateTableValue(value_td, i, j) {
        const value = this.values[i][j];
        if (value === null) {
            value_td.innerHTML = "";
        } else {
            this._updateValue(value_td, value);
        }
    }

    /**
     * Convenience method to update a single inferred scale value
     * @param {HTMLElement} value_td - The table cell to update
     * @param {number} value - The inferred scale value
     */
    _updateValue(value_td, value) {
        const exponent = Math.log10(Math.abs(value)).toFixed(1);
        value_td.innerHTML = `10<sup>${exponent}</sup>`;
    }
}

/**
 * Convenience function to get de-logged slider values from list of slider ids
 * @param {string[]} sliderIDs - Slider DOM ids
 * @returns {number[]} - Array of slider values
 */
function getSliderValues(sliderIDs) {
    return sliderIDs.map((id) => {
        const slider = document.getElementById(id);
        return Math.pow(10, parseFloat(slider.value));
    });
}

/**
 * Convenience function to update slider output display
 * @param {HTMLElement} slider - slider input element
 * @param {HTMLElement} output - slider output element
 */
function updateSliderOutput(slider, output) {
    // Update slider output text
    let exponent = parseFloat(slider.value).toFixed(1);
    output.innerHTML = `10<sup>${exponent}</sup> ${output.units}`;
}

/**
 * Convenience function to add listeners to sliders to update scale table
 * @param {string[]} sliderIDs - Array of slider DOM ids
 * @param {function} inferredScales - Function to calculate implied scales
 * @param {function} calculationFunction - Function to calculate table values
 * @param {ScaleTable} scaleTable - ScaleTable instance to update
 */
function addListeners(
    sliderIDs,
    inferredScales,
    calculationFunction,
    scaleTable
) {
    sliderIDs.forEach((id) => {
        const slider = document.getElementById(id);
        const output_id = id.replace("-slider", "-output");
        const output = document.getElementById(output_id);
        slider.addEventListener("input", function () {
            // Update slider output text
            updateSliderOutput(slider, output);
            // Update the scale table
            const sliderValues = getSliderValues(sliderIDs);
            const values = calculationFunction(...sliderValues);
            const inferredScaleValues = inferredScales(...sliderValues);
            scaleTable.inferredScaleValues = inferredScaleValues;
            scaleTable.values = values;
            scaleTable.update();
        });
    });
}

/**
 * Convenience function to fix the initial output display for each slider
 * before adding to DOM
 * @param {HTMLElement[]} allSliders - Array of slider row elements
 */
function initializeOutputs(allSliders) {
    allSliders.forEach((row) => {
        const input = row.querySelector('input[type="range"]');
        const output = row.querySelector("output");
        let value = parseFloat(input.value);
        let units = output.units;
        output.innerHTML = `10<sup>${value.toFixed(1)}</sup> ${units}`;
    });
}
