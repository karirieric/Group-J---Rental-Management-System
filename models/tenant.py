# models/tenant.py

from models.user import User

class Tenant(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password)
        self.leases = []

    def view_leases(self):
        if not self.leases:
            print("No leases found.")
            return
        for lease in self.leases:
            print(f"Lease ID: {lease.lease_id} for Property: {lease.property.property_name}")
            lease.view_payments()

