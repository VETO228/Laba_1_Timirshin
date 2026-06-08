import sqlite3
from datetime import date

DATABASE = 'nootbook.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def get_all_tasks():
    conn = get_db_connection()
    messages = conn.execute(
        'SELECT * FROM entries ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    return messages


def get_tasks(item_id):
    conn = get_db_connection()
    messages = conn.execute(
        'SELECT * FROM entries WHERE id = ?', (item_id,)
    ).fetchone()
    conn.close()
    return messages


def add_tasks(title, content, created_at):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO entries (title, content, created_at) VALUES (?, ?, ?)', (title, content, created_at)
    )
    conn.commit()
    conn.close()


def delete_tasks(item_id):
    conn = get_db_connection()
    conn.execute(
        'DELETE FROM entries WHERE id = ?', (item_id,)
    )
    conn.commit()
    conn.close()


def get_task_count():
    """
    Возвращает общее количество сообщений.
    """
    conn = get_db_connection()
    cursor = conn.execute('SELECT COUNT(*) FROM entries')
    count = cursor.fetchone()[0]
    conn.close()
    return count


def update_task(title, content, created_at, item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE entries SET title = ?, content = ?, created_at = ? WHERE id = ?', (title, content, created_at, item_id)
    )
    conn.commit()

    updated_task = cursor.execute(
        'SELECT * FROM entries WHERE id = ?', (item_id,)
    ).fetchone()

    conn.close()
    return updated_task
