class ScaleTable {
    /**
     * Initialize a ScaleTable instance
     * @param {string[][]} ids - Array of element ids
     * @param {string[][]} terms - Array of term labels
     * @param {string[][]} values - Array of corresponding values
     * @param {string[][]} units - Array of corresponding units
     */
    constructor(ids, terms, values, units) {
        this.ids = ids;
        this.terms = terms;
        this.values = values;
        this.units = units;
        const table = document.createElement("table");

        const tbody = document.createElement("tbody");
        for (let i = 0; i < terms.length; i++) {
            const tr = document.createElement("tr");
            for (let j = 0; j < terms[i].length; j++) {
                const td = document.createElement("td");
                td.id = this.ids[i][j];
                this._updateElement(td, i, j);
                tr.appendChild(td);
            }
            tbody.appendChild(tr);
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
                const td = document.getElementById(this.ids[i][j]);
                this._updateElement(td, i, j);
                MathJax.typesetPromise([td]);
            }
        }
    }

    /**
     * Convenience method to update a single table element
     * @param {HTMLElement} td - The table cell to update
     * @param {number} i - The row index
     * @param {number} j - The column index
     */
    _updateElement(td, i, j) {
        const term = this.terms[i][j];
        const value = this.values[i][j];
        const unit = this.units[i][j];
        const scale = Math.log10(Math.abs(value));
        td.innerHTML = `\\(${term} \\sim 10^{${scale.toFixed(1)}}\\) ${unit}`;
    }
}

// Define some convenience sliders
