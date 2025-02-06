from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Хранение вопросов и ответов в памяти
questions = []
answers = {}

@app.route('/')
def index():
    return render_template('index.html', questions=questions, answers=answers)

@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        content = request.form['content']
        questions.append(content)
        # Создаем пустой список для ответов на этот вопрос
        answers[len(questions) - 1] = []
        return redirect(url_for('index'))
    return render_template('ask.html')

@app.route('/answer/<int:question_id>', methods=['GET', 'POST'])
def answer(question_id):
    if request.method == 'POST':
        content = request.form['content']
        # Добавляем ответ в список
        answers[question_id].append(content)
        return redirect(url_for('index'))
    return render_template('answer.html', question_id=question_id, question=questions[question_id])

if __name__ == '__main__':
    app.run(debug=True)