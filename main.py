import psycopg2


def create_tables():
    with psycopg2.connect(database='clients', user='postgres', password='55555') as conn:
        with conn.cursor() as cur:
            cur.execute(f"CREATE TABLE IF NOT EXISTS clients ( "
                        f"client_id SERIAL PRIMARY KEY, "
                        f"name VARCHAR(15) NOT NULL, "
                        f"surname VARCHAR(15) NOT NULL, "
                        f"email VARCHAR(25) UNIQUE);"
                        f"CREATE TABLE IF NOT EXISTS phone_numbers ( "
                        f"phone_number_id SERIAL PRIMARY KEY, "
                        f"client_id INTEGER REFERENCES clients(client_id), "
                        f"phone_number VARCHAR(15) NOT NULL);")
            conn.commit()
            print('Таблицы созданы...')
    conn.close()
    print()


def add_new_client():
    print('- Добавить нового клиента -')
    name = input('Введите имя: ')
    surname = input('Введите фамилию: ')
    email = input('Введите email: ')
    phone_number = input('Введите номер телефона: ')
    with psycopg2.connect(database='clients', user='postgres', password='55555') as conn:
        with conn.cursor() as cur:
            cur.execute(f"INSERT INTO clients (name, surname, email) "
                        f"VALUES ('{name}','{surname}','{email}'); "
                        f"SELECT * FROM clients;")
            client_id = cur.fetchall()[-1][0]
            if phone_number != '':
                cur.execute(f"INSERT INTO phone_numbers (client_id, phone_number) "
                            f"VALUES ({client_id}, '{phone_number}');")
                conn.commit()
                print(f'Новый клиент успешно добавлен')
    conn.close()
    print()


def print_clients_info():
    print('- Показать основную информацию о клиентах -')
    with psycopg2.connect(database='clients', user='postgres', password='55555') as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM clients;")
            clients_info = cur.fetchall()
            print('|' + '№'.center(5) + '|' + 'Имя'.center(15) + '|' + 'Фамилия'.center(15) + '|' +
                  'e-mail'.center(25) + '|')
            print('=' * 65)
            for row in range(len(clients_info)):
                print('|' + str(clients_info[row][0]).center(5) + '|' + clients_info[row][1].center(15) + '|' +
                      clients_info[row][2].center(15) + '|' + clients_info[row][3].center(25) + '|')
    conn.close()
    print()


def add_phone_number():
    print('- Добавить номер телефона -')
    client_id = input('Укажите id клиента: ')
    new_phone_number = input('Укажите номер телефона: ')
    with psycopg2.connect(database='clients', user='postgres', password='55555') as conn:
        with conn.cursor() as cur:
            cur.execute(f"INSERT INTO phone_numbers (client_id, phone_number)"
                        f"VALUES ({client_id},'{new_phone_number}');")
            conn.commit()
            print(f'Номер телефона успешно добавлен')
    conn.close()
    print()


def update_client_info():
    print('- Изменить основные данные о клиенте -')
    client_id = input('Укажите id клиента: ')
    new_name = input('Введите новое [Имя] или оставьте поле пустым: ')
    new_surname = input('Введите новую [Фамилию] или оставьте поле пустым: ')
    new_email = input('Введите новую [Почту] или оставьте поле пустым: ')
    updates_str = ''
    if new_name != '':
        updates_str += f"name='{new_name}'"
    if new_surname != '':
        updates_str += f", surname='{new_surname}'"
    if new_email != '':
        updates_str += f", email='{new_email}'"
    with psycopg2.connect(database='clients', user='postgres', password='55555') as conn:
        with conn.cursor() as cur:
            cur.execute(f"UPDATE clients SET {updates_str} WHERE client_id={client_id};")
            conn.commit()
            print('Данные успешно изменены')
    conn.close()
    print()


def show_client_phone_numbers():
    print('- Показать номера телефонов клиентов -')
    with psycopg2.connect(database='clients', user='postgres', password='55555') as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM clients;")
            client_info = cur.fetchall()
            for client in client_info:
                print(f'Клиент {client[1]} {client[2]}')
                print('Номера телефонов:')
                cur.execute(f"SELECT * FROM phone_numbers WHERE client_id={client[0]};")
                client_phones = cur.fetchall()
                print('|' + '№'.center(5) + '|' + 'Номер телефона'.center(16) + '|')
                for client_phone in client_phones:
                    print('|' + str(client_phone[0]).center(5) + '|' + client_phone[2].center(16) + '|')
    conn.close()
    print()


def del_phone_number():
    print('- Удалить номер телефона -')
    client_id = input('Укажите id клиента: ')
    with psycopg2.connect(database='clients', user='postgres', password='55555') as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM clients WHERE client_id={client_id};")
            client_info = cur.fetchone()
            print(f'Клиент {client_info[1]} {client_info[2]}')
            print('Номера телефонов:')
            cur.execute(f"SELECT * FROM phone_numbers WHERE client_id={client_id};")
            client_phones = cur.fetchall()
            print('|' + '№'.center(5) + '|' + 'Номер телефона'.center(16) + '|')
            for client_phone in client_phones:
                print('|' + str(client_phone[0]).center(5) + '|' + client_phone[2].center(16) + '|')
            phone_number_id = input('Введите id удаляемого номера: ')
            cur.execute(f"DELETE FROM phone_numbers WHERE phone_number_id={phone_number_id};")
            conn.commit()
            print('Номер телефона успешно удален')
    conn.close()
    print()


def del_client():
    print('- Удалить клиента -')
    client_id = input('Укажите id клиента: ')
    with psycopg2.connect(database='clients', user='postgres', password='55555') as conn:
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM phone_numbers WHERE client_id={client_id};"
                        f"DELETE FROM clients WHERE client_id={client_id};")
            conn.commit()
            print('Клиент успешно удален из базы')
    conn.close()
    print()


def find_client():
    print('- Найти клиента -')
    key = input('Введите поисковый запрос: ')
    with psycopg2.connect(database='clients', user='postgres', password='55555') as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT DISTINCT clients.client_id, name, surname, email, phone_number "
                        f"FROM clients "
                        f"JOIN phone_numbers "
                        f"ON clients.client_id = phone_numbers.client_id "
                        f"WHERE name LIKE '%{key}%' OR surname LIKE '%{key}%' OR email LIKE '%{key}%' "
                        f"OR phone_number LIKE '%{key}%';")
            clients_info = cur.fetchall()
            print(clients_info)
            print('|' + '№'.center(5) + '|' + 'Имя'.center(15) + '|' + 'Фамилия'.center(15) + '|' +
                  'e-mail'.center(25) + '|' + 'Номер телефона'.center(16) + '|')
            print('=' * 82)
            for client in clients_info:
                print('|' + str(client[0]).center(5) + '|' + client[1].center(15) + '|' +
                      client[2].center(15) + '|' + client[3].center(25) + '|' + client[4].center(16))
    conn.close()
    print()


def main():
    functions = {1: create_tables,
                 2: add_new_client,
                 3: add_phone_number,
                 4: update_client_info,
                 5: del_phone_number,
                 6: del_client,
                 7: find_client,
                 8: print_clients_info,
                 9: show_client_phone_numbers
                 }
    print('[1] - создать таблицы\n[2] - добавить клиента\n[3] - добавить номер телефона\n'
          '[4] - изменить сведения о клиенте\n[5] - удалить номер телефона клиента\n'
          '[6] - удалить клиента из базы\n[7] - найти клиента\n[8] - показать основную информацию о клиентах\n'
          '[9] - показать номера телефонов клиентов')
    function = int(input('Выберите функцию: '))
    functions[function]()


if __name__ == '__main__':
    while True:
        main()
