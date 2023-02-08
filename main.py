import psycopg2
from pprint import pprint


def create_db(connect, cursor):
    """Creating a database structure (tables)."""
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(40) NOT NULL,
                last_name VARCHAR(40) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE);
                """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS phones(
                phone_id SERIAL PRIMARY KEY,
                client_id INTEGER NOT NULL REFERENCES clients(client_id) ON DELETE CASCADE,
                phone VARCHAR(40)); 
                """)

    connect.commit()


def delete_table(cursor):
    """Deletes tables before starting."""
    cursor.execute("""
            DROP TABLE clients, phones CASCADE;
            """)


def add_new_client(cursor, first_name=None, last_name=None, email=None, phone=None):
    """Adding information about a new client."""
    cursor.execute("""
            INSERT INTO clients(first_name, last_name, email) 
            VALUES (%s, %s, %s)
            RETURNING client_id, first_name, last_name;
            """, (first_name, last_name, email))
    new_client = cur.fetchone()
    if phone is not None:
        cur.execute("""
                INSERT INTO phones(client_id, phone)
                VALUES (%s, %s)
                RETURNING phone;
                """, (new_client[0], phone))
        cur.fetchone()
    print('Клиент', *new_client[1:], 'добавлен(-а) в таблицу.')


def add_phone_number(cursor, client_id, phone):
    """Adding a phone number for an existing client."""
    cursor.execute("""
            INSERT INTO phones(client_id, phone)
            VALUES (%s, %s)
            RETURNING client_id, phone;
            """, (client_id, phone))
    number = cur.fetchone()
    print(f'Для клиента с id {number[0]} добавлен номер телефона {number[1]}.')


def change_info_clients(connect, cursor, client_id, first_name=None, last_name=None, email=None, phone=None):
    """Changing customer data."""
    if first_name is not None:
        cursor.execute("""
            UPDATE clients SET first_name=%s WHERE client_id=%s;
            """, (first_name, client_id))
    if last_name is not None:
        cur.execute("""
            UPDATE clients SET last_name=%s WHERE client_id=%s;
            """, (last_name, client_id))
    if email is not None:
        cur.execute("""
            UPDATE clients SET email=%s WHERE client_id=%s;
            """, (email, client_id))
    if phone is not None:
        cur.execute("""
            UPDATE phones SET phone=%s WHERE client_id=%s;
            """, (phone, client_id))
    connect.commit()
    print(f'Данные клиента с id {client_id} изменены.')


def delete_phone_client(connect, cursor, client_id, phone):
    """Deletes a phone for an existing client."""
    cursor.execute("""
            DELETE FROM phones WHERE client_id=%s AND phone=%s;
            """, (client_id, phone))
    connect.commit()
    print(f'Номер телефона {phone} для клиента с id {client_id} удален.')


def delete_client(connect, cursor, client_id):
    """Deletes an existing client"""
    cursor.execute("""
            DELETE FROM clients WHERE client_id=%s;
            """, (client_id,))
    connect.commit()
    print(f'Клиент с id {client_id} удален.')
    #  запрос сохраняет изменения без commit
    # cur.execute("""
    #         SELECT * FROM clients;
    #         """)
    # pprint(cur.fetchall())


def find_client(cursor, first_name=None, last_name=None, email=None, phone=None):
    """Finds a client based on his data."""
    if first_name is not None:
        cursor.execute("""
                SELECT c.client_id, c.first_name, c.last_name, c.email, p.phone FROM clients AS c
                LEFT JOIN phones AS p ON c.client_id = p.client_id
                WHERE c.first_name LIKE %s""", (first_name,))
        pprint(cur.fetchall())
    if last_name is not None:
        cursor.execute("""
                SELECT c.client_id, c.first_name, c.last_name, c.email, p.phone FROM clients AS c
                LEFT JOIN phones AS p ON c.client_id = p.client_id
                WHERE c.last_name LIKE %s""", (last_name,))
        pprint(cur.fetchall())
    if email is not None:
        cursor.execute("""
                SELECT c.client_id, c.first_name, c.last_name, c.email, p.phone FROM clients AS c
                LEFT JOIN phones AS p ON c.client_id = p.client_id
                WHERE c.email LIKE %s""", (email,))
        pprint(cur.fetchall())
    if phone is not None:
        cursor.execute("""
                SELECT c.client_id, c.first_name, c.last_name, c.email, p.phone FROM clients AS c
                LEFT JOIN phones AS p ON c.client_id = p.client_id
                WHERE p.phone LIKE %s""", (phone,))
        pprint(cur.fetchall())


def all_clients(cursor):
    """View all customer information."""
    cursor.execute("""
            SELECT c.client_id, first_name, last_name, email, phone FROM clients AS c
            LEFT JOIN phones AS p ON c.client_id = p.client_id
            ORDER BY client_id;
            """)
    pprint(cur.fetchall())


if __name__ == '__main__':
    with psycopg2.connect(database='info_clients_db', user='postgres', password='***********') as conn:
        with conn.cursor() as cur:
            delete_table(cur)
            create_db(conn, cur)
            # add_new_client(cur, 'Алекс', 'Тучнев', 'tuchnev@gmail.com', '+79775662345')
            # add_new_client(cur, 'Алена', 'Петрова', 'al_petr1996@gmail.com')
            # add_new_client(cur, 'Сергей', 'Еременко', 'eremenko2023@yandex.ru', '+79225338978')
            # add_new_client(cur, 'Артур', 'Ерофеев', 'erofeev2023@yandex.ru', '+79227782566')
            # all_clients(cur)
            # add_phone_number(cur, '1', '+79365556565')
            # add_phone_number(cur, '2', '+79456887555')
            # add_phone_number(cur, '3', '+79456888855')
            # all_clients(cur)
            # change_info_clients(conn, cur, '1', 'Артур', None, 'ar_tuchnev@mail.ru')
            # change_info_clients(conn, cur, '2', None, None, 'petrova@gmail.com')
            # change_info_clients(conn, cur, '4', None, 'Большаков', None, '+79226548963')
            # all_clients(cur)
            # delete_phone_client(conn, cur, 1, '+79775662345')
            # delete_client(conn, cur, 2)
            # all_clients(cur)
            # find_client(cur, 'Артур')
            # find_client(cur, None, 'Тучнев')
            # find_client(cur, None, None, 'eremenko2023@yandex.ru')
            # find_client(cur, None, None, None, '+79456887555')
            # all_clients(cur)

    conn.close()
