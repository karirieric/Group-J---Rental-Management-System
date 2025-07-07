# models/lease.py

class Lease:
    def __init__(self, lease_id, property, tenant, start_date, end_date):
        self.lease_id = lease_id
        self.property = property    # Composition
        self.tenant = tenant        # Composition
        self.start_date = start_date
        self.end_date = end_date
        self.payments = []          # List of RentPayment objects

    def add_payment(self, payment):
        self.payments.append(payment)

    def view_payments(self):
        if not self.payments:
            print("No payments recorded.")
            return
        for payment in self.payments:
            payment.display_payment()

