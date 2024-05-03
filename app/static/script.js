document.addEventListener('DOMContentLoaded', function() {
    const cells = document.querySelectorAll('.txt-input'); // Select all cells in the Sudoku grid
    const keypadKeys = document.querySelectorAll('.keypad-key'); // Select all keypad keys

    // Add event listener to each cell in the Sudoku grid
    cells.forEach(function(cell) {
        cell.addEventListener('click', function() {
            // Remove focus from other cells
            cells.forEach(function(c) {
                c.classList.remove('focused');
            });

            // Add focus to the clicked cell
            cell.classList.add('focused');
        });
    });

    // Add event listener to each keypad key
    keypadKeys.forEach(function(key) {
        key.addEventListener('click', function() {
            // Get the number from the clicked keypad key
            const number = this.innerText;

            // Get the selected cell (if any)
            const selectedCell = document.querySelector('.focused');

            // If a cell is selected and the button clicked is not "Clear", assign the number to its value
            if (selectedCell && number !== 'Clear') {
                selectedCell.value = number;
            } else if (selectedCell && number === 'Clear') { // If "Clear" button is clicked, clear the value of the selected cell
                selectedCell.value = '';
            }
        });
    });
});