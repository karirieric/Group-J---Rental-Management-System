# models/property.py

class Property:
    def __init__(self, property_id, property_name, location, rent_amount):
        self.property_id = property_id
        self.property_name = property_name
        self.location = location
        self.rent_amount = rent_amount

    def display_property(self):
        print(f"Property ID: {self.property_id}")
        print(f"Name: {self.property_name}")
        print(f"Location: {self.location}")
        print(f"Rent: {self.rent_amount}")

