from services.database import Database
from models.user import Customer, Admin

class AuthService:
    def __init__(self):
        self.db = Database().connection

#------------------Registraion--------------------------
    def register(self, name, username, email, contact, password, confirm_password, role):
        if password != confirm_password:
            raise ValueError("Passwords do not match")

        cursor = self.db.cursor()
        cursor.execute("""
                       INSERT INTO users (name, username, email, contact, password, role) VALUES (?, ?, ?, ?, ?, ?)""", 
                       (name, username, email, contact, password, role))
        self.db.commit()

#--------------------Login---------------------------
    def login(self, username, password):
        cursor = self.db.cursor()
        cursor.execute("""
                       SELECT * FROM users WHERE username=? AND password=?""", (username, password))
        user = cursor.fetchone()

        if not user:
            return None

        if user["role"] == "admin":
            return Admin(
                user["user_id"],
                user["name"],
                user["username"],
                user["email"],
                user["contact"]
            )
        
        else:
            return Customer(
                user["user_id"],
                user["name"],
                user["username"],
                user["email"],
                user["contact"]
            )
