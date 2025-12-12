from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Создаем таблицу, если она еще не существует
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (?, ?, ?)", 
              (1, 'John Doe', 'john@example.com'))
    
    # Добавим вторую запись для демонстрации полосатой таблицы
    c.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (?, ?, ?)", 
              (2, 'Jane Smith', 'jane@example.com'))
    
    conn.commit()
    
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    
    return render_template('index.html', users=users)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)