
/**
 * Create a scale table for the given terms and values
 * @param {string[][]} ids - Array of element ids
 * @param {string[][]} terms - Array of term labels
 * @param {string[][]} values - Array of corresponding values
 * @returns {HTMLTableElement} - The created table element
 */
function createScaleTable(ids, terms, values) {
    const table = document.createElement('table');
    
    // Create header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    data.headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // Create body
    const tbody = document.createElement('tbody');
    data.rows.forEach(rowData => {
        const tr = document.createElement('tr');
        rowData.forEach(cellData => {
            const td = document.createElement('td');
            td.textContent = cellData;
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    
    return table;
}

// Usage
const tableData = {
    headers: ['Term', 'Scale'],
    rows: [
        ['u ∂u/∂x', '10 m/s²'],
        ['∂p/∂x', '5 Pa/m']
    ]
};
document.getElementById('container').appendChild(createTable(tableData));