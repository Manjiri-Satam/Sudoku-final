// List of functions we need :
// A function to handle the selection of cells such as selectCell(row, column)
// A function to select a number from keypad such as selectNumber(number)
// A function to clear the selected cell such as clearCell()
// A function to highlight the wrong cell such as wrongCell(cells)
// A function to start the timer when the page is loaded such as readyTimer()
// A function to update the timer such as updateTimer()
// A function to pause the timer such as pauseTimer()
// A function to open a resume pop-up page such as resume()
// A function to request a hint such as requestHint()
// A function to solve the sudoku such as solveSudoku()
// A function to reset the sudoku such as resetSudoku()
// A function to start a new puzzle such as newSudoku()

// But we also need classes for the timer such as start(), stop(), reset(), update()

keypadKeys.forEach(function(key) {
    key.addEventListener("click", function() {
        console.log("Key clicked:", this.dataset.number);
        const number = this.dataset.number;
        const selectedCell = document.querySelector(".sudoku-cell:focus");
        console.log("Selected cell:", selectedCell);

        if (selectedCell) {
            selectedCell.value = number;
            console.log("Value assigned to cell:", selectedCell.value);
        }
    });
});