from flask import Flask, request, jsonify, flash, Blueprint, render_template, request, session, redirect, url_for
from app.program.Solver_experiment_unified import UnifiedSolver

main = Blueprint('main', __name__)

@main.route('/')
def home():
    username = session.get('username', 'Guest')
    return render_template('home.html', username=username)

@main.route('/easy')
def easy():
    sudoku = '...3.........8.19.71..5...44......7337...65.8..61.........154......97.....5......'
    return render_template('play.html', difficulty='easy',sudoku=list(sudoku))

@main.route('/medium')
def medium():
    sudoku = '....7.....6...2.494.1..6..7.298....6...15....1.4...5..........1..65.....2...4....'
    return render_template('play.html', difficulty='medium',sudoku=list(sudoku))

@main.route('/hard')
def hard():
    sudoku = '5..1.764..........413......2.....15.6.......7....754..7.4....6.86.2...1.......3.5'
    return render_template('play.html', difficulty='hard',sudoku=list(sudoku))

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