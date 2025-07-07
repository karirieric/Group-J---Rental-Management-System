# models/user.py

class User:
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password

    def display_user_info(self):
        print(f"User ID: {self.user_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")

