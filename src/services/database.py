import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("car_rental.db")
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            contact TEXT,
            password TEXT,
            role TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            car_id TEXT PRIMARY KEY,
            brand TEXT,
            model TEXT,
            year INTEGER,
            mileage INTEGER,
            available_now INTEGER,
            min_rent_period INTEGER,
            max_rent_period INTEGER
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            car_id TEXT,
            start_date TEXT,
            end_date TEXT,
            status TEXT,
            total_price REAL
        )
        """)

        self.connection.commit()
