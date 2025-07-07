# models/administrator.py

from models.user import User

class Administrator(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password)
        self.properties = []
        self.tenants = []
        self.leases = []

    def add_property(self, property_obj):
        self.properties.append(property_obj)
        print(f"Property '{property_obj.property_name}' added successfully!")

    def register_tenant(self, tenant_obj):
        self.tenants.append(tenant_obj)
        print(f"Tenant '{tenant_obj.name}' registered successfully!")

    def assign_lease(self, lease_obj):
        self.leases.append(lease_obj)
        print(f"Lease ID '{lease_obj.lease_id}' assigned successfully!")

    def record_rent_payment(self, lease_obj, payment_obj):
        lease_obj.add_payment(payment_obj)
        print(f"Payment of {payment_obj.amount} recorded successfully!")

