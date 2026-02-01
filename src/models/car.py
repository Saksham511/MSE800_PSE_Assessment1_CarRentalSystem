class Car:

    def __init__(self, brand, model, year, mileage, min_rent_period, max_rent_period, daily_rate):
        
        self.brand = brand
        self.model = model
        self.year = year
        self.mileage = mileage
        self.available_now = True
        self.min_rent_period = min_rent_period
        self.max_rent_period = max_rent_period
        self.daily_rate = daily_rate

    def mark_rented(self):
        self.available_now = False

    def mark_returned(self):
        self.available_now = True
