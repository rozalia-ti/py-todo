from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            created TEXT,
            updated TEXT,
            tags TEXT
        )
    ''')
    
    if conn.execute('SELECT COUNT(*) FROM tasks').fetchone()[0] == 0:
        conn.execute('''
            INSERT INTO tasks (title, description, created, updated, tags) 
            VALUES 
            ('Buy groceries', 'Milk, eggs, bread', '2023-10-15', '2023-10-16', 'home,shopping'),
            ('Finish report', 'Complete quarterly analysis', '2023-10-14', '2023-10-15', 'work,urgent'),
            ('Call dentist', 'Schedule appointment', '2023-10-13', '2023-10-13', 'health')
        ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    tags = request.form['tags']
    now = datetime.now().strftime('%Y-%m-%d')
    
    conn = get_db()
    conn.execute('''
        INSERT INTO tasks (title, description, created, updated, tags) 
        VALUES (?, ?, ?, ?, ?)
    ''', (title, description, now, now, tags))
    conn.commit()
    conn.close()
    
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = get_db()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)