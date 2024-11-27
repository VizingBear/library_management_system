import sqlite3

import database


def create_book(title, author, year, user_id):
    with sqlite3.connect(database.database) as conn:
        cursor = conn.cursor()

        try:
            title_id = (cursor.execute('SELECT id FROM title WHERE content = (?)', (title))).fetchone()[0]
        except:
            title_id = (cursor.execute('INSERT INTO title(content) VALUES (?) RETURNING id;', (title,) ).fetchone()[0])

        try:
            author_id = ((cursor.execute('SELECT id FROM author WHERE name = (?)', (author))).fetchone()[0])
        except:
            author_id = (cursor.execute('INSERT INTO author(name) VALUES (?) RETURNING id;', (author,) ).fetchone()[0])

        try:
            year_id = ((cursor.execute('SELECT id FROM year WHERE date = (?)', (year))).fetchone()[0])
        except:
            year_id = (cursor.execute('INSERT INTO year(date) VALUES (?) RETURNING id;', (year,) ).fetchone()[0])

        book_id = int(
            cursor.execute(
                '''
                    INSERT INTO book(title_id, author_id, year_id, status_id, user_id) 
                    VALUES (?,?,?,?,?) 
                    RETURNING id;
                    ''',
                (int(title_id), int(author_id), int(year_id), 1, int(user_id))
            ).fetchone()[0]
        )

        book_data = f'title = {title}, author = {author}, year = {year}, status = В наличии'

        cursor.execute('INSERT INTO book_text(book_id, book_data) VALUES (?,?)', (book_id, book_data) )

        conn.commit()


def finding_book(title:str=None, author:str=None, year:int=None) -> list:
    with sqlite3.connect(database.database) as conn:
        cursor = conn.cursor()

        if title:
            data = (
                cursor.execute('''
                    SELECT book_text.book_data 
                    FROM book 
                    JOIN book_text ON book.id = book_text.book_id
                    JOIN title ON book.title_id = title.id
                    WHERE title.content LIKE ?
                    ''', ('%'+title+'%', )
                )
            ).fetchall()

        if author:
            data = (
                cursor.execute('''
                    SELECT book_text.book_data 
                    FROM book 
                    JOIN book_text ON book.id = book_text.book_id
                    JOIN author ON book.author_id = author.id
                    WHERE author.name LIKE ?
                    ''', ('%'+author+'%',)
                               )
            ).fetchall()

        if year:
            data = (
                cursor.execute('''
                    SELECT book_text.book_data 
                    FROM book 
                    JOIN book_text ON book.id = book_text.book_id
                    JOIN year ON book.year_id = year.id
                    WHERE year.date= (?)
                    ''', (year,)
                               )
            ).fetchall()

        return data


def update_book(book_id:int, status:int):
    with sqlite3.connect(database.database) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE book SET status_id = ? WHERE id = ?', (status,book_id))
        book_data = (cursor.execute('SELECT book_data FROM book_text WHERE book_id = ?', (book_id,))).fetchone()[0]
        text_status = 'В наличии' if status == 1 else 'Выдана'
        curent_book_data = book_data.replace('В наличии',f'{text_status}').replace('Выдана',f'{text_status}')
        cursor.execute('UPDATE book_text SET book_data = ? WHERE book_id = ?', (curent_book_data,book_id))

        conn.commit()


def drop_book(book_id):
    with sqlite3.connect(database.database) as conn:
        cursor = conn.cursor()

        try:
            (cursor.execute('SELECT id FROM book WHERE id = (?)', (book_id))).fetchone()[0]
        except:
            raise Exception

        cursor.execute('DELETE FROM book WHERE id = (?)', (book_id))
