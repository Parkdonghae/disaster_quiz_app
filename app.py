

import os
from flask import Flask, render_template, request, redirect, url_for, session
import json
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ✅ JSON 경로를 절대 경로로 맞춤
basedir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(basedir, 'quiz_data.json'), encoding='utf-8') as f:
    QUIZ_DATA = json.load(f)

@app.route('/')
def home():
    categories = list(QUIZ_DATA.keys())
    return render_template('home.html', categories=categories)

@app.route('/start/<category>')
def start(category):
    if category not in QUIZ_DATA:
        return redirect(url_for('home'))
    session['category'] = category
    session['score'] = 0
    session['current'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    category = session.get('category')
    if not category or category not in QUIZ_DATA:
        return redirect(url_for('home'))

    questions = QUIZ_DATA[category]

    if request.method == 'POST':
        selected = request.form.get('option')
        if selected and selected == questions[session['current']]['answer']:
            session['score'] += 1
        session['current'] += 1

        if session['current'] >= len(questions):
            return redirect(url_for('result'))

    current_q = questions[session['current']]
    return render_template('quiz.html', question=current_q, current=session['current']+1, total=len(questions))

@app.route('/result')
def result():
    score = session.get('score', 0)
    total = len(QUIZ_DATA.get(session.get('category', ''), []))
    return render_template('result.html', score=score, total=total)

if __name__ == '__main__':
    app.run()