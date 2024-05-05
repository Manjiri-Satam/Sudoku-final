import pandas as pd
import os
from flask import Flask, request, jsonify, flash, Blueprint, render_template, request, session, redirect, url_for
from app.program.Solver_experiment_unified import UnifiedSolver
import random

project_root = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(project_root, 'sudoku_results.csv')
sudoku_data = pd.read_csv(csv_path)
sudoku_list = sudoku_data.to_dict(orient='records')
print(sudoku_list[:5])

def get_sudoku_by_difficulty(sudoku_list, level):
    # Filter the Sudoku puzzles by the specified difficulty level
    filtered_sudokus = [s for s in sudoku_list if s['difficulty_level'] == level]
    if not filtered_sudokus:
        raise ValueError(f"No Sudoku puzzles found for difficulty: {level}")
    # Return a random Sudoku puzzle from the filtered list
    return random.choice(filtered_sudokus)

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/easy')
def easy():
    try:
        # Pass both sudoku_list and the level ('easy') to the function
        puzzle = get_sudoku_by_difficulty(sudoku_list, 'easy')
        return render_template('play.html', difficulty='easy', sudoku=list(puzzle['sudoku_generated']))
    except ValueError as e:
        flash(str(e), 'error')
        return render_template('home.html')

@main.route('/medium')
def medium():
    try:
        # Ensure the correct level ('medium') is passed
        puzzle = get_sudoku_by_difficulty(sudoku_list, 'medium')
        return render_template('play.html', difficulty='medium', sudoku=list(puzzle['sudoku_generated']))
    except ValueError as e:
        flash(str(e), 'error')
        return render_template('home.html')

@main.route('/hard')
def hard():
    try:
        puzzle = get_sudoku_by_difficulty(sudoku_list, 'hard')  # Pass the level
        return render_template('play.html', difficulty='hard', sudoku=list(puzzle['sudoku_generated']))
    except ValueError as e:
        flash(str(e), 'error')
        return render_template('home.html')

@main.route('/play')
def play():
    return render_template('play.html')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/instructions')
def instructions():
    return render_template('instructions.html')


@main.route('/contact')
def contact():
    return render_template('contact.html')


@main.route('/setting')
def setting():
    return render_template('setting.html')


@main.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        flash('Logged in successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('login.html')

@main.route('/validate-sudoku', methods=['POST'])
def validate_sudoku():
    data = request.get_json()
    if not data or 'grid' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    # Assuming grid is a 2D list of integers representing the Sudoku board
    grid = data['grid']
    solver = UnifiedSolver(grid)  # Initialize your solver with the board
    results = solver.check_grid_items()

    # Determine if the Sudoku solution is valid
    is_valid = all(all(row) for row in results)
    return jsonify({'is_valid': is_valid})