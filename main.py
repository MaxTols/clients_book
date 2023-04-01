import psycopg2

from pprint import pprint


def create_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client(
        client_id SERIAL PRIMARY KEY,
        first_name VARCHAR(40) NOT NULL,
        last_name VARCHAR(40) NOT NULL,
        email VARCHAR(50) NOT NULL UNIQUE
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phone(
        id SERIAL PRIMARY KEY,
        phone VARCHAR(15) NOT NULL UNIQUE,
        client_id INTEGER NOT NULL REFERENCES client(client_id)
    );
    """)
    conn.commit()


def add_client(first_name, last_name, email):
    cur.execute("""
    INSERT INTO client(first_name, last_name, email) 
    VALUES(%s, %s, %s);
    """, (first_name, last_name, email))
    print('Клиент добавлен')
    conn.commit()


def add_phone(client_id, phone):
    cur.execute("""
    INSERT INTO phone(client_id, phone) 
    VALUES(%s, %s)
    """, (client_id, phone))
    print('Телефон добавлен')
    conn.commit()


def change_client(text, client_id, first_name=None, last_name=None, email=None, phone=None):
    if text == 'phone':
        last_phone = (input('Введите предыдущий номер: '))
        cur.execute("""
        UPDATE phone SET phone=%s
        WHERE client_id=%s AND phone=%s;
        """, (phone, client_id, last_phone))
    else:
        cur.execute("""
        UPDATE client SET first_name=%s, last_name=%s, email=%s 
        WHERE client_id=%s;
        """, (first_name, last_name, email, client_id))
    print('Запись обновлена')
    conn.commit()


def delete_phone(client_id, phone):
    cur.execute("""
    DELETE FROM phone WHERE client_id=%s AND phone=%s;
    """, (client_id, phone))
    print('Телефон удален')
    conn.commit()


def delete_client(client_id):
    cur.execute("""
    DELETE FROM phone WHERE client_id=%s;
    """, (client_id,))
    cur.execute("""
    DELETE FROM client WHERE client_id=%s;
    """, (client_id,))
    print('Клиент удален')
    conn.commit()


def find_client(first_name=None, last_name=None, email=None, phone=None):
    cur.execute("""
    SELECT * FROM client c
    LEFT JOIN phone p ON c.client_id = p.client_id
    WHERE first_name=%s OR last_name=%s OR email=%s OR phone=%s;
    """, (first_name, last_name, email, phone))
    pprint(cur.fetchall())


def delete_table():
    cur.execute("""
    DROP TABLE phone;
    DROP TABLE client;
    """)
    print('Таблицы удалены!')


def all_info():
    cur.execute("""
    SELECT * FROM client c
    LEFT JOIN phone p ON c.client_id = p.client_id;
    """)
    pprint(cur.fetchall())


with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    with conn.cursor() as cur:
        # create_db()
        # add_client('Tony', 'Stark', 'stark@mail.ru')
        # add_client('Steve', 'Rogers', 'capitan@america.ru')
        # add_client('Bruce', 'Wayne', 'Batmen@inbox.com')
        # add_phone(1, '+11111111111')
        # add_phone(1, '+13333333333')
        # add_phone(2, '+15555555555')
        # change_client('phone', 1, phone='+19999999999')
        # change_client('client', 1, first_name='Iron', last_name="Man", email='iron@ya.com')
        # delete_phone(2, '+15555555555')
        # delete_client(3)
        # find_client(phone='+13333333333')
        # find_client(first_name='Steve')
        # delete_table()
        all_info()

conn.close()
