from flask import Flask, render_template, request, redirect, url_for, session
from collections import defaultdict
import os
import sys
from questions import questions, axis_types

app = Flask(__name__)
app.secret_key = 'your-secret-key'

def calculate_type(scores):
    result = ""
    for axis, (t1, t2) in axis_types.items():
        result += t1 if scores[axis] >= 0 else t2
    return result

@app.route('/')
def index():
    session.clear()
    session['answers'] = []
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    q = int(request.args.get('q', 0))
    if q >= len(questions):
        return redirect(url_for('result'))
    return render_template('quiz.html', question=questions[q]['text'], q=q, total=len(questions))

@app.route('/answer', methods=['POST'])
def answer():
    q = int(request.form['q'])
    val = int(request.form['value'])
    answers = session.get('answers', [])
    if len(answers) == q:
        answers.append(val)
    else:
        answers[q] = val
    session['answers'] = answers
    return redirect(url_for('quiz', q=q+1))

@app.route('/result')
def result():
    scores = defaultdict(int)
    for i, val in enumerate(session.get('answers', [])):
        axis = questions[i]['axis']
        scores[axis] += val
    type_code = calculate_type(scores)
    return render_template('result.html', type_code=type_code)

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
    except Exception:
        port = 5000
    try:
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    except SystemExit:
        print('Server failed to start. Check environment and port settings.')
        sys.exit(1)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
