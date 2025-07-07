# models/rent_payment.py

class RentPayment:
    def __init__(self, payment_id, amount, payment_date):
        self.payment_id = payment_id
        self.amount = amount
        self.payment_date = payment_date

    def display_payment(self):
        print(f"Payment ID: {self.payment_id}")
        print(f"Amount: {self.amount}")
        print(f"Payment Date: {self.payment_date}")

