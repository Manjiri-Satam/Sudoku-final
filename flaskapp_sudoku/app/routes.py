from flask import flash, Blueprint, render_template, request, session, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
def home():
    username = session.get('username', 'Guest')
    return render_template('home.html', username=username)

@main.route('/easy')
def easy():
    return render_template('play.html', difficulty='easy')

@main.route('/medium')
def medium():
    return render_template('play.html', difficulty='medium')

@main.route('/hard')
def hard():
    return render_template('play.html', difficulty='hard')

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