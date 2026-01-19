from services.database import Database
from models.car import Car
from datetime import datetime

class RentalService:
    def __init__(self):
        self.db = Database().connection

    def add_car(self, brand, model, year, mileage, min_days, max_days):
        car = Car(brand, model, year, mileage, min_days, max_days)
        cursor = self.db.cursor()
        cursor.execute("""
        INSERT INTO cars VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            car.car_id,
            car.brand,
            car.model,
            car.year,
            car.mileage,
            int(car.available_now),
            car.min_rent_period,
            car.max_rent_period
        ))
        self.db.commit()

    def list_available_cars(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM cars WHERE available_now=1")
        return cursor.fetchall()

    def calculate_price(self, start_date, end_date, daily_rate=50):
        days = (datetime.strptime(end_date, "%Y-%m-%d") -
                datetime.strptime(start_date, "%Y-%m-%d")).days
        if days > 7:
            return days * daily_rate * 0.9
        return days * daily_rate

    def create_booking(self, user_id, car_id, start_date, end_date):
        total_price = self.calculate_price(start_date, end_date)
        cursor = self.db.cursor()

        cursor.execute("""
        INSERT INTO bookings (user_id, car_id, start_date, end_date, status, total_price)
        VALUES (?, ?, ?, ?, 'PENDING', ?)
        """, (user_id, car_id, start_date, end_date, total_price))

        cursor.execute("""
        UPDATE cars SET available_now=0 WHERE car_id=?
        """, (car_id,))

        self.db.commit()

    def update_booking_status(self, booking_id, approve=True):
        status = "APPROVED" if approve else "REJECTED"
        cursor = self.db.cursor()
        cursor.execute("""
        UPDATE bookings SET status=? WHERE booking_id=?
        """, (status, booking_id))
        self.db.commit()
