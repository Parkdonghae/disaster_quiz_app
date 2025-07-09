from flask import Flask, render_template, request, redirect, url_for, session
import json
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

import os

basedir = os.path.dirname(__file__)

def load_quiz_data():
    with open(os.path.join(basedir, 'quiz_data.json'), encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def home():
    QUIZ_DATA = load_quiz_data()
    categories = list(QUIZ_DATA.keys())
    return render_template('home.html', categories=categories)


@app.route('/start/<category>')
def start(category):
    session['category'] = category
    session['score'] = 0
    session['current'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    category = session.get('category')
    if not category:
        return redirect(url_for('home'))

    QUIZ_DATA = load_quiz_data()

    if request.method == 'POST':
        selected = request.form['option']
        correct = QUIZ_DATA[category][session['current']]['answer']
        if selected == correct:
            session['score'] += 1
        session['current'] += 1

    if session['current'] >= len(QUIZ_DATA[category]):
        return redirect(url_for('result'))

    question = QUIZ_DATA[category][session['current']]
    options = question['options']
    return render_template('quiz.html', question=question, options=options)

@app.route('/result')
def result():
    score = session.get('score', 0)
    total = session.get('current', 1)
    return render_template('result.html', score=score, total=total)

if __name__ == '__main__':
    app.run(debug=True)
