from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from models import User, Note

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    
    # Create users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Create notes table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            data_create TEXT NOT NULL,
            data_update TEXT NOT NULL,
            tags TEXT
        )
    ''')
    
    # Create user_notes junction table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            note_id TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (note_id) REFERENCES notes (id)
        )
    ''')
    
    # Create default user if none exists
    if conn.execute('SELECT COUNT(*) FROM users').fetchone()[0] == 0:
        conn.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            ('Default User', 'user@example.com', 'password123')
        )
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    
    # Get default user (first user)
    user_row = conn.execute('SELECT * FROM users LIMIT 1').fetchone()
    
    # Get all notes for this user
    notes = conn.execute('''
        SELECT n.* FROM notes n
        JOIN user_notes un ON n.id = un.note_id
        WHERE un.user_id = ?
    ''', (user_row['id'],)).fetchall()
    
    conn.close()
    
    # Convert to Note objects
    note_objects = []
    for note in notes:
        try:
            note_obj = Note(
                id=note['id'],
                title=note['title'],
                discription=note['description'],
                data_create=note['data_create'],
                data_update=note['data_update'],
                tags=note['tags']
            )
            note_objects.append(note_obj)
        except Exception as e:
            print(f"Error creating Note object: {e}")
    
    return render_template('index.html', notes=note_objects)

@app.route('/add', methods=['POST'])
def add_note():
    title = request.form['title']
    description = request.form['description']
    tags = request.form.get('tags', '')
    note_id = datetime.now().strftime('%Y%m%d%H%M%S%f')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = get_db()
    
    try:
        # Get default user
        user_row = conn.execute('SELECT * FROM users LIMIT 1').fetchone()
        
        # Create and insert note
        note = Note(
            id=note_id,
            title=title,
            discription=description,
            data_create=current_time,
            data_update=current_time,
            tags=tags
        )
        
        # Insert into notes table
        conn.execute('''
            INSERT INTO notes (id, title, description, data_create, data_update, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (note.id, note.title, note.discription, note.data_create, note.data_update, note.tags))
        
        # Link note to user
        conn.execute('''
            INSERT INTO user_notes (user_id, note_id)
            VALUES (?, ?)
        ''', (user_row['id'], note.id))
        
        conn.commit()
    except Exception as e:
        print(f"Error adding note: {e}")
        conn.rollback()
    finally:
        conn.close()
    
    return redirect('/')

@app.route('/delete/<note_id>')
def delete_note(note_id):
    conn = get_db()
    
    try:
        conn.execute('DELETE FROM user_notes WHERE note_id = ?', (note_id,))
        conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        conn.commit()
    except Exception as e:
        print(f"Error deleting note: {e}")
        conn.rollback()
    finally:
        conn.close()
    
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)