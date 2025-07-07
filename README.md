# Group J - Rental Management System

**BSD 2302 - Python Programming | CAT 2**  
**Group J Members:**

- Alek Deng (21/08298)
- Eric Kariri (22/00580)
- Muad Shafii (23/01427)
- Mike Gichia (23/01626)

## Project Overview

A comprehensive Python GUI application for managing rental properties, built using Object-Oriented Programming principles. The system provides separate interfaces for administrators and tenants, enabling efficient property management, lease tracking, and payment recording.

## Features

### Admin Features

- **Property Management**: Add, view, and manage rental properties
- **Tenant Registration**: Register new tenants with secure authentication
- **Lease Assignment**: Assign properties to tenants with lease agreements
- **Payment Recording**: Track and record rent payments
- **Reports**: View system statistics and recent activities

### Tenant Features

- **Lease Information**: View current lease details and property information
- **Payment History**: Access complete payment history
- **User-Friendly Interface**: Intuitive design for easy navigation

## Technology Stack

- **Language**: Python 3.7+
- **GUI Framework**: Tkinter
- **Database**: SQLite3
- **Image Processing**: Pillow (PIL)
- **Architecture**: Object-Oriented Programming

## Project Structure

```
rental-management-system/
├── Main.py                 # Main application file
├── database.py            # Database setup and management
├── setup_and_run.py       # Setup and launch script
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── models/               # OOP model classes
│   ├── user.py
│   ├── administrator.py
│   ├── tenant.py
│   ├── property.py
│   ├── lease.py
│   └── rent_payment.py
├── admin_bg.png          # Admin dashboard background
├── tenant_bg.png         # Tenant dashboard background
├── logo.png              # Application logo
└── rental_management.db  # SQLite database (auto-generated)
```

## Quick Start

### Option 1: Clone from GitHub (For Lecturer/Evaluator)
```bash
# Clone the repository
git clone https://github.com/karirieric/Group-J---Rental-Management-System.git

# Navigate to the project directory
cd Group-J---Rental-Management-System

# Install dependencies
pip install -r requirements.txt

# Run the application
python Main.py
```

### Option 2: Automated Setup (If already downloaded)
```bash
python Main.py
```

### Option 3: Manual Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python Main.py
   ```

## Login Credentials

### Administrator Access

- **Email**: `groupj@python.com`
- **Password**: `groupj`

## Database Schema

The system uses SQLite with the following tables:

### Properties

- `property_id` (Primary Key)
- `property_name`
- `location`
- `rent_amount`
- `created_date`

### Tenants

- `tenant_id` (Primary Key)
- `name`
- `email` (Unique)
- `password`
- `phone`
- `created_date`

### Leases

- `lease_id` (Primary Key)
- `property_id` (Foreign Key)
- `tenant_id` (Foreign Key)
- `start_date`
- `end_date`
- `status`
- `created_date`

### Payments

- `payment_id` (Primary Key)
- `lease_id` (Foreign Key)
- `amount`
- `payment_date`
- `payment_method`
- `notes`
- `created_date`

## Object-Oriented Design

The system implements core OOP principles:

### Classes

- **User**: Base class for system users
- **Administrator**: Inherits from User, manages system operations
- **Tenant**: Inherits from User, views personal information
- **Property**: Represents rental properties
- **Lease**: Links tenants to properties
- **RentPayment**: Records payment transactions

### Relationships

- **Inheritance**: Administrator and Tenant inherit from User
- **Composition**: Lease contains Property and Tenant references
- **Association**: Payment is associated with Lease

## Future Enhancements

- [ ] Property maintenance tracking
- [ ] Advanced reporting with charts
- [ ] Email integration

### Common Issues

1. **Import Errors**

   ```bash
   pip install customtkinter pillow
   ```

2. **Database Issues**
   - Delete `rental_management.db` and restart the application

3. **Image Loading Errors**
   - The system creates placeholder images automatically if originals are missing

4. **Permission Errors**
   - Ensure you have write permissions in the application directory

## Support

For technical support or questions about this project, please contact any of the group members through our school respective emails.

## License

This project is created for educational purposes as part of the BSD 2302 Python Programming course at KCA University.

---

## © 2025 Group J - BSD 2302 Python Programming - KCA University