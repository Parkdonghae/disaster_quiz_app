from flask import Flask, render_template, request, redirect, url_for, session
import json
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Render 서버에서 파일 경로 문제 방지
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'quiz_data.json')

with open(JSON_PATH, encoding='utf-8') as f:
    QUIZ_DATA = json.load(f)

@app.route('/')
def home():
    categories = list(QUIZ_DATA.keys())
    return render_template('home.html', categories=categories)

@app.route('/start/<category>')
def start(category):
    session['category'] = category
    session['score'] = 0
    session['current'] = 0
    session['wrong'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    category = session.get('category')
    if not category:
        return redirect(url_for('home'))

    questions = QUIZ_DATA[category]
    current = session.get('current', 0)

    if request.method == 'POST':
        selected = request.form.get('option')
        correct = questions[current]['answer']
        if selected == correct:
            session['score'] += 1
        else: 
            wrong_list= session_get('wrong', []) wrong_list.append({'question' : questions[current]['question'], 
                 'selected': selected, , 'correct': correct })
        session['wrong'] = wrong_list
        session['current'] += 1
        current = session['current']

    if current >= len(questions):
        return redirect(url_for('result'))

    question = questions[current]
    return render_template('quiz.html', question=question['question'], options=question['options'], current=current+1, total=len(questions))

@app.route('/result')
def result():
    score = session.get('score', 0)
    category = session.get('category')
    total = len(QUIZ_DATA.get(category, []))
    wrong_answers = session.get('wrong',[])  
    return render_template('result.html', score=score, total=total, wrong_answers=wrong_answers)