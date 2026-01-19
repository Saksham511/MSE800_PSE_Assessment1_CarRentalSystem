class Booking:
    def __init__(self, booking_id, user_id, car_id, start_date, end_date, status, total_price):
        self.booking_id = booking_id
        self.user_id = user_id
        self.car_id = car_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.total_price = total_price
