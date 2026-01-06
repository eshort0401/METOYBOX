class ScaleTable {
    /**
     * Initialize a ScaleTable instance
     * @param {string} containerID - The container element id
     * @param {string[][]} terms - Array of term labels
     * @param {string[][]} values - Array of corresponding values
     * @param {string[][]} units - Array of corresponding units
     */
    constructor(containerID, terms, values, units) {
        
        // Build row and column ids programmatically
        this.ids = terms.map((row, i) =>
            row.map((term, j) => `${containerID}-${i}-${j}`)
        );

        this.terms = terms;
        this.values = values;
        this.units = units;
        const table = document.createElement("table");

        const tbody = document.createElement("tbody");
        for (let i = 0; i < terms.length; i++) {
            const label_tr = document.createElement("tr");
            const value_tr = document.createElement("tr");
            for (let j = 0; j < terms[i].length; j++) {
                const label_td = document.createElement("td");
                const value_td = document.createElement("td");
                // Set the value td to have the id for updating later
                value_td.id = this.ids[i][j];
                // Initialize the table label
                const term = this.terms[i][j];
                label_td.innerHTML = `\\(${term}\\)`;
                this._updateValue(value_td, i, j);
                label_tr.appendChild(label_td);
                value_tr.appendChild(value_td);
            }
            tbody.append(label_tr, value_tr);
        }
        table.appendChild(tbody);
        this.table = table;
    }

    /**
     * Update the scale table in the DOM with new values. Assumes the table
     * has already been created and added to the DOM.
     */
    update() {
        for (let i = 0; i < this.ids.length; i++) {
            for (let j = 0; j < this.ids[i].length; j++) {
                const value_td = document.getElementById(this.ids[i][j]);
                this._updateValue(value_td, i, j);
            }
        }
    }

    /**
     * Convenience method to update a single table value
     * @param {HTMLElement} td - The table cell to update
     * @param {number} i - The row index
     * @param {number} j - The column index
     */
    _updateValue(value_td, i, j) {
        const value = this.values[i][j];
        const unit = this.units[i][j];
        if (value === null) {
            value_td.innerHTML = "";
        } else {
            const exponent = Math.log10(Math.abs(value)).toFixed(1);
            value_td.innerHTML = `10<sup>${exponent}</sup> ${unit}`;
        }
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
 * @param {function} calculationFunction - Function to calculate table values
 * @param {ScaleTable} scaleTable - ScaleTable instance to update
 */
function addListeners(sliderIDs, calculationFunction, scaleTable) {
    sliderIDs.forEach((id) => {
        const slider = document.getElementById(id);
        const output_id = id.replace("-slider", "-output");
        const output = document.getElementById(output_id);
        slider.addEventListener("input", function () {
            // Update slider output text
            updateSliderOutput(slider, output);
            // Update the scale table
            const sliderValues = getSliderValues(sliderIDs);
            const tableValues = calculationFunction(...sliderValues);
            scaleTable.values = tableValues;
            scaleTable.update();
        });
    });
}

/**
 * Convenience function to fix the initial output display for each slider
 * before adding to DOM
 * @param {HTMLElement[]} allSliders - Array of slider row elements
 */
function initializeValues(allSliders) {
    allSliders.forEach((row) => {
        const input = row.querySelector('input[type="range"]');
        const output = row.querySelector("output");
        let value = parseFloat(input.value);
        let units = output.units;
        output.innerHTML = `10<sup>${value.toFixed(1)}</sup> ${units}`;
    });
}
