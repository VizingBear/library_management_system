import os
import sqlite3

import database


def check_user(login: str, password: str):
    with sqlite3.connect(database.database) as conn:
        cursor = conn.cursor()

        if not os.environ.get('HASH_PASS'):
            import config
            password_hash = config.HASH_PASS
        else:
            password_hash = os.environ.get('HASH_PASS')

        cursor.execute(
            'SELECT * FROM user WHERE login = (?) AND password = (?)', (login, f'{password_hash}{password}')
        )

        user = cursor.fetchone()
        if not user:
            print('Вы ввели неверный логин или пароль')
            raise Exception

        return user[0]


def login():
    print("Авторизация")
    username = input('\nВведите логин: ')
    password = input('\nВыберите пароль: ')

    if not username or not password:
        print('Вы не ввели логин или пароль')
        login()
    try:
        user_id = check_user(username,password)
    except:
        login()

    return user_id
