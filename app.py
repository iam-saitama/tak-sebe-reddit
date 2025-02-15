from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import os

app = Flask(__name__)

# Путь к БД
DATABASE = 'qa.db'

# Подключение к БД
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Для доступа к данным по имени столбца
        db.row_factory = sqlite3.Row
    return db

# Закрытие соединения с БД
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# БД (создание таблиц)
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.executescript(f.read())
        db.commit()

# Главная страница
@app.route('/')
def index():
    db = get_db()
    questions = db.execute('SELECT * FROM question').fetchall()  # Получаем все вопросы
    return render_template('index.html', questions=questions)

# Страница для вопросов
@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        content = request.form['content']
        db = get_db()
        db.execute('INSERT INTO question (content) VALUES (?)', (content,))
        db.commit()
        return redirect(url_for('index'))
    return render_template('ask.html')

# Страница для ответов
@app.route('/answer/<int:question_id>', methods=['GET', 'POST'])
def answer(question_id):
    db = get_db()
    if request.method == 'POST':
        content = request.form['content']
        db.execute('INSERT INTO answer (content, question_id) VALUES (?, ?)', (content, question_id))
        db.commit()
        return redirect(url_for('index'))
    question = db.execute('SELECT * FROM question WHERE id = ?', (question_id,)).fetchone()
    answers = db.execute('SELECT * FROM answer WHERE question_id = ?', (question_id,)).fetchall()
    return render_template('answer.html', question=question, answers=answers)

# Запуск приложения
if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()  # Инициализация БД при первом запуске
    app.run(debug=True)