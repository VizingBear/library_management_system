import os

from auth import login
from crud import create_book, drop_book, finding_book, update_book
from database import create_db


def add_book(user_id: int):
    title = input('\nВведите название книги: ')
    author = input('\nВведите автора (по примеру Иванов Иван Иванович: ')
    year = input('\nВведите год: ')

    try:
        year = int(year)
        create_book(title, author, year, user_id)
        print('\n------Книга добавлена-------')
    except:
        print('-----Вы ввели некорректные данные, книга не была записана-----')


def delete_book():
    try:
        book_id = int(input('\nВведите id книги: '))
    except:
        print('-----Вы ввели не число------')
        raise Exception

    try:
        drop_book(book_id)
        print('-----Книга удалена-------')
    except:
        print('-----Книги с таким идентефикатором не найдено------')


def find_book():
    #TODO: add pagination
    ask = input('\nВыберите по какому параметру вы хотите искать: Название(1), Автор(2), Год(3), Выйти(0): ')
    if ask == '1':
        title = input('\nВведите название: ')
        books:list = finding_book(title=title)
    elif ask == '2':
        author = input('\nВведите автора: ')
        books:list = finding_book(author=author)
    elif ask == '3':
        year = input('\nВведите название: ')
        try:
            year = int(year)
            books:list = finding_book(year=year)
        except:
            print('\n-----Вы ввели некорректные данные-----')

    elif ask == '0':
        print('\nЗавершаю программу')
        return None
    else:
        print('\nНет такой команды')
        find_book()

    if not books:
        print('-----Книги не найдены----')
        return None


def change_book():
    try:
        book_id = int(input('\nВведите id книги: '))
        status = int(input('\nКакой статус хотите присвоить:В наличии(1) или Выдана(2): '))
    except:
        print('\n-----Вы ввели не число------')
        return None

    update_book(book_id, status)

    try:
        update_book(book_id, status)
    except:
        print('\n----Вы ввели некорректные данные-----')


def main(user_id:int):
    print('\nДля выполнения действия введите соответствующее число')
    ask = input('\nВыберите действие: Добавить книгу(1), Удаление книги(2), Поиск книги(3), Изменение статуса книги(4), Выйти(0): ')
    if ask == '1':
        add_book(user_id)
        main(user_id)
    elif ask == '2':
        delete_book()
        main(user_id)
    elif ask == '3':
        find_book()
        main(user_id)
    elif ask == '4':
        change_book()
        main(user_id)
    elif ask == '0':
        print('\nЗавершаю программу')
        return None
    else:
        print('Нет такой команды')
        main(user_id)


if __name__ == '__main__':
    create_db()
    user_id = login()
    main(user_id)
