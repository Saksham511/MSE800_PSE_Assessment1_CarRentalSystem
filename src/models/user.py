class User:
    def __init__(self, user_id, name, username, email, contact, role):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.email = email
        self.contact = contact
        self.role = role

#----------created two inheritance of User-------------
class Customer(User):
    def __init__(self, user_id, name, username, email, contact):
        super().__init__(user_id, name, username, email, contact, "customer")


class Admin(User):
    def __init__(self, user_id, name, username, email, contact):
        super().__init__(user_id, name, username, email, contact, "admin")
