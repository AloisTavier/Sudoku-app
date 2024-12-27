# app.py
from flask import Flask, render_template, jsonify, request
import sudoku_generator as sg
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    difficulty = request.json.get('level')
    grid, _ = sg.grid_sudoku()
    unsolved = sg.unsolved_grid(grid.copy(), level=difficulty)
    grids = [unsolved.tolist(), grid.tolist()]
    return jsonify(grids=grids)
    # return jsonify(grid=unsolved.tolist())

@app.route('/validate', methods=['POST'])
def validate():
    grid = np.array(request.json.get('grid'))
    valid = sg.check_grid(grid) and not sg.chek0inGrid(grid)
    return jsonify(valid=valid)

@app.route('/validmove', methods=['POST'])
def nonValid():
    grid = np.array(request.json.get('grid'))
    validated = not sg.check_grid(grid)[1]
    problem = sg.check_grid(grid)[0]
    validation = [validated, problem]
    return jsonify(validation=validation)

if __name__ == '__main__':
    app.run(debug=True)
