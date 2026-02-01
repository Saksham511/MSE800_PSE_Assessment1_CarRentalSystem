import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("car_rental.db")
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

#----------------creating tables------------------------
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
                       car_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       brand TEXT,
                       model TEXT,
                       year INTEGER,
                       mileage INTEGER,
                       available_now BOOLEAN,
                       min_rent_period INTEGER,
                       max_rent_period INTEGER,
                       daily_rate REAL DEFAULT 0
                       )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS bookings (
                       booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER,
                       car_id TEXT,
                       start_date TEXT,
                       end_date TEXT,
                       return_date TEXT,
                       status TEXT,
                       total_price REAL,
                       extra_charge REAL DEFAULT 0
                       )
                       """)

        self.connection.commit()
