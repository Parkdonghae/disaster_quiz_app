from flask import Flask, render_template, request, redirect, url_for, session
import json
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

with open('quiz_data.json', encoding='utf-8') as f:
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
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    category = session.get('category')
    if not category:
        return redirect(url_for('home'))

    if request.method == 'POST':
        selected = int(request.form['option'])
        answer = session.get('answer')
        correct = selected == answer
        session['score'] += int(correct)
        session['current'] += 1

        if session['current'] >= 1:
            return redirect(url_for('result'))
        else:
            return redirect(url_for('quiz'))

    question = random.choice(QUIZ_DATA[category])
    session['answer'] = question['answer']
    return render_template('quiz.html', category=category, question=question)

@app.route('/result')
def result():
    score = session.get('score', 0)
    total = session.get('current', 1)
    return render_template('result.html', score=score, total=total)

if __name__ == '__main__':
    app.run(debug=True)
