import os
import sqlite3

info_messages = ['Введите Название книги', 'Введите ФИО автора', 'Введите год публикации книги']


def main():
    if not os.path.isfile('book.db'):
        connection()
    key = True
    while key:
        menu()
        inp_command = input('\nВаш выбор:\t')
        print()
        if not inp_command.isdigit():
            print('Введите число\n')
            continue
        else:
            inp_command = int(inp_command)
            if inp_command == 1:
                select_all()
                waiting()
            elif inp_command == 2:
                search_by_author()
                waiting()
            elif inp_command == 3:
                search_by_name()
                waiting()
            elif inp_command == 4:
                get_book_info()
                waiting()
            elif inp_command == 5:
                update_book()
                waiting()
            elif inp_command == 6:
                delete_book()
                waiting()
            elif inp_command == 7:
                key = False
            else:
                print('Введите целое число от 1 до 6\n')
                continue


def waiting():
    input('Веедите любой символ для возврата\t')
    print()


def menu():
    print('Картотека книг\n')
    print('1\tВывести все содержимое библиотеки')
    print('2\tПоиск по автору')
    print('3\tПоиск по названию книги')
    print('4\tДобавление книги в библиотеку')
    print('5\tРедактирование книги в библиотеке')
    print('6\tУдаление книги из библиотеки')
    print('7\tВыход')


def get_book_info():
    book_info = []
    get_iter = iter(info_messages)
    for i in range(len(info_messages)):
        book_info.append(input(next(get_iter) + '\t'))
    add_book(book_info)


def search_by_author():
    key = True
    while key:
        author = input('Введите ФИО автора (0 для возврата):\t')
        if author and author != 0:
            search(author=author)
            key = False
        elif author == 0:
            break


def search_by_name():
    key = True
    while key:
        name = input('Введите название книги (0 для возврата):\t')
        if name and name != '0':
            search(name=name)
            key = False
        elif name == '0':
            break


def update_book():
    key = True
    while key:
        id = input('Введите id книги которую хотите изменить (0 для возврата):\t')
        if id.isdigit() and id != '0':
            name = input('Введите название книги (ENTER для пропуска):\t')
            author = input('Введите ФИО автора (ENTER для пропуска):\t')
            year = input('Введите год публикации книги (ENTER для пропуска):\t')
            key = False
            if not update_db(id, name, author, year):
                print('Введен некорректный id, повторите попытку')
                key = True
        else:
            break


def delete_book():
    key = True
    while key:
        id = input('Введите id книги которую удалить (0 для возврата):\t')
        if id.isdigit() and id != '0':
            key = False
            if not delete_row(id):
                print('Введен некорректный id, повторите попытку')
                key = True
        else:
            break


def connection():
    conn = sqlite3.connect('book.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE books(id integer PRIMARY KEY, name text, author text, year text)')
    conn.close()


def select_all():
    conn = sqlite3.connect('book.db')
    cursor = conn.cursor()
    cursor.execute('select * from books')
    rows = cursor.fetchall()
    for row in rows:
        print(f'id:\t{row[0]}\n\t' + \
              'Название:' + '\t' * 2 + f'{row[1]}\n\t' + \
              'Автор:' + '\t' * 3 + f'{row[2]}\n\t' + \
              f"Год публикации:\t{row[3]}")
    print()
    conn.close()


def search(author='', name=''):
    conn = sqlite3.connect('book.db')
    cursor = conn.cursor()
    if len(author):
        cursor.execute(f'select * from books where author like "%{author}%"')
    else:
        cursor.execute(f'select * from books where name like "%{name}%"')
    rows = cursor.fetchall()
    for row in rows:
        print(f'id:\t{row[0]}\n\t' + \
              'Название:' + '\t' * 2 + f'{row[1]}\n\t' + \
              'Автор:' + '\t' * 3 + f'{row[2]}\n\t' + \
              f"Год публикации:\t{row[3]}")
    print()
    conn.close()


def add_book(book_info):
    conn = sqlite3.connect('book.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books(id, name, author, year) VALUES(null, ?, ?, ?)', book_info)
    conn.commit()
    conn.close()


def update_db(id, name='', author='', year=''):
    conn = sqlite3.connect('book.db')
    cursor = conn.cursor()
    cursor.execute(f'select * from books where id = "{id}"')
    rows = cursor.fetchall()
    if len(rows):
        if len(name) and not len(author) and not len(year):
            cursor.execute(f'update books set name = "{name}" where id = "{id}"')
        elif not len(name) and len(author) and not len(year):
            cursor.execute(f'update books set author = "{author}" where id = "{id}"')
        elif not len(name) and not len(author) and len(year):
            cursor.execute(f'update books set year = "{year}" where id = "{id}"')
        elif len(name) and len(author) and not len(year):
            cursor.execute(f'update books set name = "{name}", author = "{author}" where id = "{id}"')
        elif len(name) and len(year) and not len(author):
            cursor.execute(f'update books set name = "{name}", year = "{year}" where id = "{id}"')
        elif len(author) and len(year) and not len(name):
            cursor.execute(f'update books set author = "{author}", year = "{year}" where id = "{id}"')
        else:
            cursor.execute(f'update books set name = "{name}", author = "{author}", year = "{year}" where id = "{id}"')
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False


def delete_row(id):
    conn = sqlite3.connect('book.db')
    cursor = conn.cursor()
    cursor.execute(f'select * from books where id = "{id}"')
    rows = cursor.fetchall()
    if len(rows):
        cursor.execute(f'delete from books where id = "{id}"')
        conn.commit()
        conn.close()
        return True
    else:
        return False


if __name__ == '__main__':
    main()
