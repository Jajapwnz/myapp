import sqlite3

class WarehouseDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('warehouse.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tab_1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT,
                name TEXT,
                amount INTEGER,
                unit TEXT,
                date TEXT,
                doc TEXT,
                location TEXT,
                expiration TEXT,
                contacts TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tab_3 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT,
                name TEXT,
                amount INTEGER,
                unit TEXT,
                date TEXT,
                doc TEXT,
                location TEXT,
                expiration TEXT,
                contacts TEXT
            )
        ''')

    def close(self):
        self.conn.commit()
        self.conn.close()