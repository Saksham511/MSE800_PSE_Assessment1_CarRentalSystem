from services.auth_service import AuthService
from ui.admin_menu import admin_menu
from ui.customer_menu import customer_menu

def main():

#---------object creation for using Authentication Service---------

    auth = AuthService()

    while True:
        print("""
              ***** CAR RENTAL SYSTEM *****
              1. Register
              2. Login
              3. Exit
              """)

        choice = input("Choose: ")

#-----------------Registraion-------------------------
        if choice == "1":
            name = input("Name: ")
            username = input("Username: ")
            email = input("Email: ")
            contact = input("Contact: ")
            password = input("Password: ")
            confirm_password = input("Confirm Password: ")
            role = input("Role (admin/customer): ").lower()

        #-----role validation-----
            if role not in ("admin", "customer"):
                print("Invalid role.")
                continue

            try:
                auth.register(
                    name,
                    username,
                    email,
                    contact,
                    password,
                    confirm_password,
                    role
                )
                print("Registration successful.")
            except ValueError as e:
                print(f"Registration failed: {e}")

#--------------------Login-------------------------------
        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")

            user = auth.login(username, password)

            if user:
                print(f"Welcome {user.name}")
                if user.role == "admin":
                    admin_menu()
                else:
                    customer_menu(user)
            else:
                print("Invalid credentials.")

#------------------exit---------------------------
        else:
            print("Thank you for visiting. Have a good day!")
            break

if __name__ == "__main__":
    main()
