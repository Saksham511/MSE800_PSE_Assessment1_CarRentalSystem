from services.database import Database
from models.car import Car
from datetime import datetime

class RentalService:
    def __init__(self):
        self.db = Database().connection

#----------------------CAR CRUD--------------------------
    def add_car(self, brand, model, year, mileage, min_days, max_days, daily_rate):
        car = Car(brand, model, year, mileage, min_days, max_days, daily_rate)
        cursor = self.db.cursor()
        cursor.execute("""
                       INSERT INTO cars(brand, model, year, mileage, available_now, min_rent_period, max_rent_period, daily_rate) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                       (car.brand,
                        car.model,
                        car.year,
                        car.mileage,
                        car.available_now,
                        car.min_rent_period,
                        car.max_rent_period,
                        car.daily_rate
                        ))
        self.db.commit()

    def update_car(self, car_id, mileage=None, available_now=None, min_rent_period=None, max_rent_period=None, daily_rate=None):
        cursor = self.db.cursor()
        # Update each field if value is provided
        if mileage is not None:
            cursor.execute("UPDATE cars SET mileage = ? WHERE car_id = ?", (mileage, car_id))

        if available_now is not None:
            cursor.execute("UPDATE cars SET available_now = ? WHERE car_id = ?", (int(available_now), car_id))

        if min_rent_period is not None:
            cursor.execute("UPDATE cars SET min_rent_period = ? WHERE car_id = ?", (min_rent_period, car_id))

        if max_rent_period is not None:
            cursor.execute("UPDATE cars SET max_rent_period = ? WHERE car_id = ?", (max_rent_period, car_id))

        if daily_rate is not None:
            cursor.execute("UPDATE cars SET daily_rate = ? WHERE car_id = ?", (daily_rate, car_id))

        self.db.commit()

    def delete_car(self, car_id):
        cursor = self.db.cursor()
        cursor.execute("""SELECT * FROM bookings WHERE car_id = ? AND status='APPROVED' """, (car_id,))
        if cursor.fetchone():
            raise Exception("Cannot delete car with active booking")

        cursor.execute("DELETE FROM cars WHERE car_id=?", (car_id,))
        self.db.commit()

    def list_available_cars(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM cars WHERE available_now=TRUE")
        return cursor.fetchall()

    def list_all_cars(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM cars")
        return cursor.fetchall()

    def get_car_info(self, car_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM cars WHERE car_id=?", (car_id,))
        return cursor.fetchone()

    def get_car_daily_rate(self, car_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT daily_rate FROM cars WHERE car_id=?", (car_id,))
        return cursor.fetchone()

#----------------Total price calculation--------------------
    def calculate_price(self, start, end, daily_rate):
        days = (datetime.strptime(end, "%Y-%m-%d") -
                datetime.strptime(start, "%Y-%m-%d")).days
        total = days * daily_rate
        return days, total

#-------------------BOOKING LOGIC-----------------------

    #----------Create booking by Customer---------------
    def create_booking(self, user_id, car_id, start, end):
        cursor = self.db.cursor()

        car = self.get_car_daily_rate(car_id)
        if not car:
            raise Exception("Car not found")

        daily_rate = car["daily_rate"]
        days, total = self.calculate_price(start, end, daily_rate)

        cursor.execute("""
        INSERT INTO bookings (user_id, car_id, start_date, end_date, status, total_price)
        VALUES (?, ?, ?, ?, 'PENDING', ?)
        """, (user_id, car_id, start, end, total))

        self.db.commit()

    #-------------approve booking by admin---------------
    def approve_booking(self, booking_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM bookings WHERE booking_id=?", (booking_id,))
        booking = cursor.fetchone()

        cursor.execute("SELECT available_now FROM cars WHERE car_id=?", (booking["car_id"],))
        car = cursor.fetchone()

        if not car["available_now"]:
            raise Exception("Sorry, another user booked this first")

        cursor.execute("UPDATE bookings SET status='APPROVED' WHERE booking_id=?", (booking_id,))
        cursor.execute("UPDATE cars SET available_now=FALSE WHERE car_id=?", (booking["car_id"],))
        self.db.commit()

    def view_booking_status(self, user_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM bookings WHERE user_id=?", (user_id,))
        return cursor.fetchall()
    
    def list_pending_bookings(self):
        cursor = self.db.cursor()
        cursor.execute(""" SELECT * FROM bookings WHERE status='PENDING' """)
        return cursor.fetchall()
    
    #----------------return car by customer------------------    
    def return_car(self, booking_id, return_date):
        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM bookings WHERE booking_id=?", (booking_id,))
        booking = cursor.fetchone()

        cursor.execute("SELECT daily_rate FROM cars WHERE car_id=?", (booking["car_id"],))
        car = cursor.fetchone()

        daily_rate = car["daily_rate"]
        late_fee = daily_rate * 1.20  # +20% charge

        end = datetime.strptime(booking["end_date"], "%Y-%m-%d")
        returned = datetime.strptime(return_date, "%Y-%m-%d")

        late_days = (returned - end).days
        extra = late_days * late_fee if late_days > 0 else 0

        cursor.execute("""UPDATE bookings SET return_date=?, extra_charge=?, status='Returned' WHERE booking_id=? """, 
                       (return_date, extra, booking_id))

        cursor.execute("UPDATE cars SET available_now=TRUE WHERE car_id=?", (booking["car_id"],))
        self.db.commit()
