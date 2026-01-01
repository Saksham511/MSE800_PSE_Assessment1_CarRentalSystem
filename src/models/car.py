class Car:
    car_counter=0
    def __init__(self,brand:str,model:str,year:int,mileage:int,min_rent_period:int,max_rent_period:int):
        Car.car_counter+=1
        self.car_id= f"C{Car.car_counter:03d}"
        self.brand=brand
        self.model=model
        self.year=year
        self.mileage=mileage
        self.available_now=True
        self.min_rent_period=min_rent_period
        self.max_rent_period=max_rent_period
    
    def mark_rented(self):
        self.available_now=False

    def mark_returned(self):
        self.available_now=True
