// static/script.js
let sol = Array.from({ length: 9 }, () => Array(9).fill(0));
let gridunsolved = Array.from({ length: 9 }, () => Array(9).fill(0));
let control = 0;
function generateGrid(level) {
    fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ level: level })
    })
    .then(response => response.json())
    .then(data => {displayGrid(data.grids[0]);sol = data.grids[1];gridunsolved = data.grids[0];});
    console.log(sol);
}
function solvedGrid() {
    if (control === 0){
        displayGrid(sol);
        control = 1;
    }
    else{
        displayGrid(gridunsolved);
        control = 0;
    }
}

function displayGrid(grid) {
    const container = document.getElementById('sudoku-grid');
    container.innerHTML = '';  // Clear previous grid

    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            const cell = document.createElement('input');
            cell.type = 'text';
            cell.maxLength = 1;
            cell.value = grid[i][j] !== 0 ? grid[i][j] : '';
            cell.dataset.row = i;
            cell.dataset.col = j;

            if (j%3 === 0){cell.style.borderLeft = '3.5px solid black';}
            if (i%3 === 0){cell.style.borderTop = '3.5px solid black';}
            if (grid[i][j] !== 0) {
                cell.style.backgroundColor = '#d0d0d0';
            }
            if (i===8){cell.style.borderBottom = '3.5px solid black';}
            if (j===8){cell.style.borderRight = '3.5px solid black';}

            cell.oninput = function () {
                // checks if the input is a number
                if (!/^[1-9]$/.test(cell.value)) {
                    cell.value = '';
                    return;
                }
                checkGrid(cell);
            };

            container.appendChild(cell);
        }
    }
}

function checkGrid(cell) {
    const inputs = document.querySelectorAll('#sudoku-grid input');
    let grid = Array.from({ length: 9 }, () => Array(9).fill(0));

    inputs.forEach(input => {
        const row = input.dataset.row;
        const col = input.dataset.col;
        grid[row][col] = input.value ? parseInt(input.value) : 0;
    });
    gridunsolved = grid;

    fetch('/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ grid: grid })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.valid);
        if (data.valid) {
            alert("Congratulations! Sudoku Solved!");
        }
    });
    fetch('/validmove', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ grid: grid })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.validation);
        if (data.validation[1]) {
            let text = cell.value + " is not a valid move! " + "Check the " + data.validation[1] + " ;)";
            alert(text);
            cell.value = '';
        }
    });
}