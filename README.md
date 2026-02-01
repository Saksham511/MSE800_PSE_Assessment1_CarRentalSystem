Yoobee College of Creative Innovation

# Subject: MSE800 Professional Software Engineering 
# Assessment1 Car Rental System

--------------------------Student details---------------------------
Developer: Saksham Shrestha
Student ID: 270775519
github: https://github.com/Saksham511

-------------------------Project Overview----------------------------

Car Rental System is designed using OOP features and Database query. It is console based and developed using python.
The basic idea of this project is the customers can view the available cars and make booking, then the admin view the
booking and decide whether to approve booking or not.


--------------------------System Used--------------------------

1. Python 3.x: Ensure you have Python installed. You can check this by running python --version in your terminal.
2. Libraries: This system uses standard Python libraries only. No external pip install is required.
    a. sqlite3: For database management.
    b. datetime: For calculating rental periods and late fees.

------------------------Installation Steps------------------------

1. clone the git link https://github.com/Saksham511/MSE800_PSE_Assessment1_CarRentalSystem
2. Install python or check version 
    python --version
3. Activate virtual environment by running this script on command line
    venv\Scripts\activate
4. Ensure the models/, services/, and ui/ folders are present alongside main.py.
5. Run the System: Navigate to the root directory in your terminal and execute python main.py.

------------------------Database Initialization---------------------------

Database Initialization: On the first run, the system automatically creates a file named car_rental.db. 
This file stores all users, cars, and bookings. The database schema is automatically initialized when the 
application starts using Database class. No manual database setup is required.

---------------------------File Architecture------------------------------

The system follows a tiered architecture to separate concerns. Below is the purpose of each file:

1. main.py: The entry point. Handles the primary login/registration loop and routes users to their specific menus.
2. user.py: Defines the User base class and Admin/Customer subclasses using inheritance.
3. car.py: Defines the attributes of a vehicle (ID, brand, model, daily rate).
4. booking.py: Defines the structure of a rental transaction.
5. database.py: Handles SQLite3 connection and initializes tables (Users, Cars, Bookings).
6. auth_service.py: Manages user authentication, password validation, and session creation.
7. rental_service.py: The core logic hub. Handles CRUD operations, price calculations, and late-fee logic.
8. admin_menu.py: The interface for Administrators to manage inventory and approve rentals.
9. customer_menu.py: The interface for Customers to browse, book, and return cars.
10. README.md: Project details 

----------------------------------Operational Guidance------------------------------
# For Admin

Managing Car: Use the "Add Car" option to add car into the system. You can update mileage or delete cars that 
              are no longer in service.

Approvals: Customer's bookings are "Pending" by default. Use the "Approve Booking" menu to review and authorize rentals.

# For Customers

Booking: Enter dates in YYYY-MM-DD format. The system will calculate the total cost automatically.

Returning: When returning a car, the system compares the actual return date with the scheduled end date.

Late Fees: If a car is returned late, the system applies an innovative 20% surcharge on the daily rate for every day past
           the deadline.

------------------------------Known Bugs & Issues-------------------------------------

1. Concurrent Bookings: The current version does not prevent two users from attempting to book the same car at the 
exact same millisecond. Conflict resolution occurs at the Admin Approval stage.

2. Date Overlap: The system does not currently block a second booking for a car if it is already booked for a 
future date (until the current booking is completed).

---------------------------Licensing Terms----------------------------

This software is released under the MIT License.