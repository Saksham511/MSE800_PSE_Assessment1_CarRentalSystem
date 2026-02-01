from services.rental_service import RentalService

def admin_menu():
    service = RentalService()

    while True:
        print("""
              ***** CAR RENTAL SYSTEM *****
              ________ ADMIN MENU ________
              
              1. Add Car
              2. Update Car
              3. Delete Car
              4. Approve Booking
              5. Log out
              """)

        choice = input("Choose: ")

        #----------ADD CAR----------
        if choice == "1":
            brand = input("Brand: ")
            model = input("Model: ")
            year = int(input("Year: "))
            mileage = int(input("Mileage: "))
            min_days = int(input("Min rent days: "))
            max_days = int(input("Max rent days: "))
            daily_rate = float(input("Daily rental fee: "))
            service.add_car(brand, model, year, mileage, min_days, max_days, daily_rate)
            print("Car added successfully.")

        #----------UPDATE CAR----------
        elif choice == "2":
            cars = service.list_all_cars()
            if not cars:
                print("No cars found.")
                continue

            print("\nCars:")
            for car in cars:
                status = "Available" if car["available_now"] else "Rented"
                print(
                    f"{car['car_id']} | {car['brand']} {car['model']} {car['year']} | "
                    f"Mileage: {car['mileage']} | Availability : {status} | "
                    f"Minimum rent days: {car['min_rent_period']} | Maximum rent days: {car['max_rent_period']} | "
                    f"daily rate: {car['daily_rate']}"
                )

            car_id = input("\nEnter Car ID to update: ")
            if not service.get_car_info(car_id):
                print(f"There is no car with this car id {car_id}. Enter valid car id.")
            else:
                # Ask for each field of car (blank means skip)
                mileage_input = input("Enter new mileage (leave blank to skip): ")
                available_input = input("Enter availability (yes/no, leave blank to skip): ")
                min_rent_input = input("Enter minimum rent days (leave blank to skip): ")
                max_rent_input = input("Enter maximum rent days (leave blank to skip): ")
                daily_rate_input = input("Enter daily rate (leave blank to skip): ")

                # Convert inputs or keep None if blank
                mileage = int(mileage_input) if mileage_input else None

                if available_input.lower() == "yes":
                    available_now = True
                elif available_input.lower() == "no":
                    available_now = False
                else:
                    available_now = None

                min_rent_period = int(min_rent_input) if min_rent_input else None
                max_rent_period = int(max_rent_input) if max_rent_input else None
                daily_rate = float(daily_rate_input) if daily_rate_input else None

                # Calls update_car
                service.update_car(car_id, mileage, available_now, min_rent_period, max_rent_period, daily_rate=daily_rate)

                print("Car updated successfully.")

        #----------DELETE CAR----------
        elif choice == "3":
            cars = service.list_all_cars()
            if not cars:
                print("No cars found.")
                continue

            print("\nCars:")
            for car in cars:
                print(
                    f"{car['car_id']} | {car['brand']} {car['model']} "
                    f"| Available: {car['available_now']}"
                )

            car_id = input("\nEnter Car ID to delete: ")
            if not service.get_car_info(car_id):
                print(f"There is no car with this car id {car_id}. Enter valid car id.")
            else:
                try:
                    service.delete_car(car_id)
                    print("Car deleted successfully.")
                except Exception as e:
                    print(e)

        #----------APPROVE BOOKING----------
        elif choice == "4":
            bookings = service.list_pending_bookings()
            if not bookings:
                print("No pending bookings.")
                continue

            print("\nPending Bookings:")
            for b in bookings:
                print(
                    f"Booking ID: {b['booking_id']} | Car: {b['car_id']} | "
                    f"User ID: {b['user_id']} | Period: {b['start_date']} -> {b['end_date']}"
                )

            booking_id = int(input("Enter Booking ID to approve: "))
            try:
                service.approve_booking(booking_id)
                print("Booking approved.")
            except Exception as e:
                print(e)
        
        else:
            print("Logged out.")
            break