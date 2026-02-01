from services.rental_service import RentalService
from datetime import datetime

def customer_menu(user):
    service = RentalService()

    while True:
        print(f"""
              ***** CAR RENTAL SYSTEM *****
              ___CUSTOMER MENU (User: {user.username})___
              
              1. View Available Cars
              2. Book a Car
              3. View My Bookings
              4. Return Car
              5. Log out
              """)

        choice = input("Choose: ")

        if choice == "1":
            cars = service.list_available_cars()
            if not cars:
                print("No cars available at the moment.")
            else:
                print("\nAvailable Cars:")
                for car in cars:
                    print(
                        f"{car['car_id']} | {car['brand']} {car['model']} "
                        f"Daily Fee: ${car['daily_rate']} | Min: {car['min_rent_period']} | Max: {car['max_rent_period']}"
                    )
        #------------book a car------------------
        elif choice == "2":
            cars = service.list_available_cars()
            if not cars:
                print("No cars available for booking.")
                continue

            print("\nAvailable Cars:")
            for car in cars:
                print(
                    f"{car['car_id']} | {car['brand']} {car['model']} | Daily Fee: ${car['daily_rate']}"
                    f"| Min days: {car['min_rent_period']} "
                    f"| Max days: {car['max_rent_period']}"
                )

            car_id = input("\nEnter Car ID to book: ")
            car = service.get_car_info(car_id)

            if not car:
                print("Car not found.")
                continue

            #------------date validation loop--------------
            while True:
                start = input("Start date (YYYY-MM-DD): ")
                end = input("End date (YYYY-MM-DD): ")
                try:
                    start_date = datetime.strptime(start, "%Y-%m-%d")
                    end_date = datetime.strptime(end, "%Y-%m-%d")
                    today = datetime.today()
                    if start_date < today:
                        print("Start date cannot be in the past.")
                        continue
                    if end_date <= start_date:
                        print("End date must be after start date.")
                        continue
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
            
            days, total = service.calculate_price(start, end, car["daily_rate"])

            print("\n--- Booking Summary ---")
            print(f"Rental Days: {days}")
            print(f"Daily Fee: ${car['daily_rate']}")
            print(f"Total: ${total}")
            print("Note: Delayed return will charge +20% per day extra fee.")

            confirm = input("Confirm booking? (yes/no): ").lower()
            if confirm == "yes":
                try:
                    service.create_booking(user.user_id, car_id, start, end)
                    print("Booking submitted for approval.")
                except Exception as e:
                    print(e)
            else:
                print("Booking cancelled.")

        #-------------view booking status----------------
        elif choice == "3":
            bookings = service.view_booking_status(user.user_id)
            if not bookings:
                print("No bookings found.")
            else:
                print("\nYour Bookings:")
                for b in bookings:
                    print(
                        f"Booking ID: {b['booking_id']} | "
                        f"Car: {b['car_id']} | "
                        f"Start Date: {b['start_date']} | "
                        f"End Date: {b['end_date']} | "
                        f"Status: {b['status']} | "
                        f"Total cost: ${b['total_price']} | "
                        f"Extra Charge: ${b['extra_charge']}"
                    )

        #--------------return car--------------------
        elif choice == "4":
            bookings = service.view_booking_status(user.user_id)
            if not bookings:
                print("No bookings found.")
            else:
                print("\nYour Bookings:")
                for b in bookings:
                    if b['status']=='APPROVED':
                        print(
                            f"Booking ID: {b['booking_id']} | "
                            f"Car: {b['car_id']} | "
                            f"Total cost: ${b['total_price']} | "
                            f"Extra Charge: ${b['extra_charge']}"
                        )
                        booking_id = int(input("Enter Booking ID: "))
                        return_date = input("Return date (YYYY-MM-DD): ")
                        try:
                            datetime.strptime(return_date, "%Y-%m-%d")
                            service.return_car(booking_id, return_date)
                            print("Car returned successfully.")
                        except Exception as e:
                            print(e)
                    else:
                        print("__")

        elif choice == "5":
            print("Logged out. We hope you like our services. See you soon!")
            break
        else:
            print("Invalid choice. Enter option from (1 to 5)")
