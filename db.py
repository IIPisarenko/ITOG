import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_file='orders.db'):
        """Инициализирует базу данных и создаёт необходимые таблицы."""
        self.connection = self.create_connection(db_file)
        self.create_tables()

    def create_connection(self, db_file):
        """Создаёт соединение с SQLite базой данных."""
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(f"Соединение с SQLite установлено: {db_file}")
            return conn
        except Error as e:
            print(e)

        return conn

    def create_tables(self):
        """Создаёт необходимые таблицы в базе данных."""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                FOREIGN KEY (client_id) REFERENCES clients (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
            ''')
            self.connection.commit()
        except Error as e:
            print(f"Ошибка при создании таблицы: {e}")

    def add_client(self, name, email, phone):
        """Добавляет клиента в базу данных."""
        sql = ''' INSERT INTO clients(name, email, phone)
                  VALUES(?,?,?) '''
        cur = self.connection.cursor()
        cur.execute(sql, (name, email, phone))
        self.connection.commit()
        return cur.lastrowid

    def delete_client(self, name):
        """Удаляет клиента из базы данных по имени."""
        sql = ''' DELETE FROM clients WHERE name = ? '''
        cur = self.connection.cursor()
        cur.execute(sql, (name,))
        self.connection.commit()

    def get_all_clients(self):
        """Получает всех клиентов из базы данных."""
        sql = ''' SELECT * FROM clients '''
        cur = self.connection.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def add_product(self, name, price):
        """Добавляет продукт в базу данных."""
        sql = ''' INSERT INTO products(name, price)
                  VALUES(?,?) '''
        cur = self.connection.cursor()
        cur.execute(sql, (name, price))
        self.connection.commit()
        return cur.lastrowid

    def get_all_products(self):
        """Получает все продукты из базы данных."""
        sql = ''' SELECT * FROM products '''
        cur = self.connection.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def add_order(self, order):
        """Добавляет заказ в базу данных."""
        sql = ''' INSERT INTO orders(client_id, product_id)
                  VALUES(?,?) '''
        cur = self.connection.cursor()
        cur.execute(sql, (order.client_id, order.product_id))
        self.connection.commit()
        return cur.lastrowid

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.connection:
            self.connection.close()
            print("Соединение с SQLite закрыто.")