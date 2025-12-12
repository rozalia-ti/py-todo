from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    # Add sample data
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)", 
              ('John Doe', 'john@example.com'))
    conn.commit()
    
    # Fetch data
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    
    return render_template('index.html', users=users)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)