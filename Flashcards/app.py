from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g
from functools import wraps
import sqlite3
import os

DATABASE = 'FLASHCARDSAPP.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = os.urandom(24)

app = Flask(__name__)

app.config.from_object(__name__)

app.config['DEBUG'] = True


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("You need to log in first.")
            return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            status_code = 401
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error), status_code


@app.route('/main')
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM flashcards')
    flashcards = [dict(content=row[1], answer=row[2]) for row in cur.fetchall()]
    g.db.close()
    return render_template('main.html', flashcards=flashcards)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/add', methods=['POST'])
@login_required
def add():
    content = request.form['content']
    answer = request.form['answer']
    if not content or not answer:
        flash("All fields are required. Please fill them up.")
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('INSERT INTO flashcards(content, answer) VALUES (?, ?)',
                     [request.form['content'], request.form['answer']])
        g.db.commit()
        g.db.close()
        flash('New fiche was added successfully!')
        return redirect(url_for('main'))


if __name__ == "__main__":
    app.run()
