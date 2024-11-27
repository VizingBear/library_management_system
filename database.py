import os
import sqlite3

database = 'library_management.db'

def create_db():
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY, 
                login TEXT NOT NULL,
                password TEXT NOT NULL
            )'''
        )
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS title (id INTEGER PRIMARY KEY, content TEXT NOT NULL)'
        )
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS author (id INTEGER PRIMARY KEY, name TEXT NOT NULL)'
        )
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS year (id INTEGER PRIMARY KEY, date INTEGER NOT NULL)'
        )
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS status (id INTEGER PRIMARY KEY, type TEXT NOT NULL)'
        )
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY, 
                title_id INTEGER,
                author_id INTEGER,
                year_id INTEGER,
                status_id INTEGER,
                user_id INTEGER,
                FOREIGN KEY (title_id)  REFERENCES title (id),
                FOREIGN KEY (author_id)  REFERENCES author (id),
                FOREIGN KEY (year_id)  REFERENCES year (id), 
                FOREIGN KEY (status_id)  REFERENCES status (id),
                FOREIGN KEY (user_id)  REFERENCES user (id)
            )'''
        )
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS book_text (
                book_id INTEGER PRIMARY KEY, 
                book_data TEXT NOT NULL,
                FOREIGN KEY (book_id)  REFERENCES book (id)
            )'''
        )

        if not os.environ.get('HASH_PASS'):
            import config
            password_hash = config.HASH_PASS
        else:
            password_hash = os.environ.get('HASH_PASS')

        cursor.execute(
            'DELETE FROM user WHERE login = (?)', ('admin', )
        )

        cursor.execute(
            'INSERT INTO user(login,password) VALUES (?,?)', ('admin', f'{password_hash}admin')
        )
        cursor.execute(
            'DELETE FROM status WHERE type = (?)', ('В наличии', )
        )
        cursor.execute(
            'INSERT INTO status(type) VALUES (?)', ('В наличии', )
        )
        cursor.execute(
            'DELETE FROM status WHERE type = (?)', ('Выдана', )
        )
        cursor.execute(
            'INSERT INTO status(type) VALUES (?)', ('Выдана', )
        )

        conn.commit()
