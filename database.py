import sqlite3
import os

def connect():
    """Create a connection to the SQLite database"""
    return sqlite3.connect('rental_management.db')

def setup_database():
    """Create database tables if they don't exist and add sample data"""
    conn = connect()
    cursor = conn.cursor()

    # Create properties table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS properties (
        property_id INTEGER PRIMARY KEY,
        property_name TEXT NOT NULL,
        location TEXT NOT NULL,
        rent_amount REAL NOT NULL,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create tenants table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tenants (
        tenant_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        phone TEXT,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create leases table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS leases (
        lease_id INTEGER PRIMARY KEY,
        property_id INTEGER NOT NULL,
        tenant_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        status TEXT DEFAULT 'Active',
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (property_id) REFERENCES properties (property_id),
        FOREIGN KEY (tenant_id) REFERENCES tenants (tenant_id)
    )
    ''')

    # Create payments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY,
        lease_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        payment_date TEXT NOT NULL,
        payment_method TEXT DEFAULT 'Cash',
        notes TEXT,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (lease_id) REFERENCES leases (lease_id)
    )
    ''')

    # Check if we need to add sample data
    cursor.execute("SELECT COUNT(*) FROM properties")
    if cursor.fetchone()[0] == 0:
        add_sample_data(cursor)

    conn.commit()
    conn.close()
    print("Database setup completed successfully!")

def add_sample_data(cursor):
    """Add sample data for testing"""
    
    # Sample properties
    sample_properties = [
        (1, "Sunset Villa", "123 Sunset Boulevard, Westlands", 2500.00),
        (2, "Garden Apartment", "456 Garden Road, Kilimani", 1800.00),
        (3, "City View Condo", "789 City Center, CBD", 3200.00),
        (4, "Riverside Flat", "321 River Lane, Lavington", 2100.00),
        (5, "Parkside Studio", "654 Park Avenue, Parklands", 1500.00)
    ]
    
    cursor.executemany(
        "INSERT INTO properties (property_id, property_name, location, rent_amount) VALUES (?, ?, ?, ?)",
        sample_properties
    )

    # Sample tenants
    sample_tenants = [
        (1, "John Doe", "john.doe@email.com", "password123", "+254701234567"),
        (2, "Jane Smith", "jane.smith@email.com", "secure456", "+254702345678"),
        (3, "Bob Johnson", "bob.johnson@email.com", "mypass789", "+254703456789"),
        (4, "Alice Brown", "alice.brown@email.com", "alice2024", "+254704567890"),
        (5, "Charlie Wilson", "charlie.wilson@email.com", "charlie123", "+254705678901")
    ]
    
    cursor.executemany(
        "INSERT INTO tenants (tenant_id, name, email, password, phone) VALUES (?, ?, ?, ?, ?)",
        sample_tenants
    )

    # Sample leases
    sample_leases = [
        (1, 1, 1, "2024-01-01", "2024-12-31", "Active"),
        (2, 2, 2, "2024-02-01", "2025-01-31", "Active"),
        (3, 3, 3, "2024-03-01", "2025-02-28", "Active"),
        (4, 4, 4, "2024-01-15", "2024-12-14", "Active"),
        (5, 5, 5, "2024-04-01", "2025-03-31", "Active")
    ]
    
    cursor.executemany(
        "INSERT INTO leases (lease_id, property_id, tenant_id, start_date, end_date, status) VALUES (?, ?, ?, ?, ?, ?)",
        sample_leases
    )

    # Sample payments
    sample_payments = [
        (1, 1, 2500.00, "2024-01-01", "Bank Transfer", "January rent"),
        (2, 1, 2500.00, "2024-02-01", "Bank Transfer", "February rent"),
        (3, 2, 1800.00, "2024-02-01", "Cash", "February rent"),
        (4, 2, 1800.00, "2024-03-01", "Cash", "March rent"),
        (5, 3, 3200.00, "2024-03-01", "Mobile Money", "March rent"),
        (6, 4, 2100.00, "2024-01-15", "Bank Transfer", "January rent"),
        (7, 5, 1500.00, "2024-04-01", "Cash", "April rent")
    ]
    
    cursor.executemany(
        "INSERT INTO payments (payment_id, lease_id, amount, payment_date, payment_method, notes) VALUES (?, ?, ?, ?, ?, ?)",
        sample_payments
    )

    print("Sample data added successfully!")

def get_property_stats():
    """Get property statistics"""
    conn = connect()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            COUNT(*) as total_properties,
            COUNT(CASE WHEN property_id IN (SELECT DISTINCT property_id FROM leases WHERE status = 'Active') THEN 1 END) as occupied,
            COUNT(CASE WHEN property_id NOT IN (SELECT DISTINCT property_id FROM leases WHERE status = 'Active') THEN 1 END) as vacant
        FROM properties
    """)
    
    stats = cursor.fetchone()
    conn.close()
    return {
        'total': stats[0],
        'occupied': stats[1],
        'vacant': stats[2]
    }

def get_tenant_stats():
    """Get tenant statistics"""
    conn = connect()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM tenants")
    total_tenants = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT tenant_id) FROM leases WHERE status = 'Active'")
    active_tenants = cursor.fetchone()[0]
    
    conn.close()
    return {
        'total': total_tenants,
        'active': active_tenants
    }

def get_payment_stats():
    """Get payment statistics"""
    conn = connect()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(amount), COUNT(*) FROM payments")
    result = cursor.fetchone()
    total_amount = result[0] if result[0] else 0
    total_payments = result[1]
    
    cursor.execute("""
        SELECT SUM(amount) 
        FROM payments 
        WHERE date(payment_date) >= date('now', 'start of month')
    """)
    monthly_amount = cursor.fetchone()[0] or 0
    
    conn.close()
    return {
        'total_amount': total_amount,
        'total_payments': total_payments,
        'monthly_amount': monthly_amount
    }

def backup_database(backup_path=None):
    """Create a backup of the database"""
    if backup_path is None:
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"rental_management_backup_{timestamp}.db"
    
    try:
        import shutil
        shutil.copy2('rental_management.db', backup_path)
        return True, f"Backup created: {backup_path}"
    except Exception as e:
        return False, f"Backup failed: {str(e)}"

def validate_database():
    """Validate database integrity"""
    try:
        conn = connect()
        cursor = conn.cursor()
        
        # Check if all tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['properties', 'tenants', 'leases', 'payments']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            conn.close()
            return False, f"Missing tables: {missing_tables}"
        
        # Check foreign key constraints
        cursor.execute("PRAGMA foreign_key_check")
        fk_violations = cursor.fetchall()
        
        conn.close()
        
        if fk_violations:
            return False, f"Foreign key violations found: {fk_violations}"
        
        return True, "Database validation successful"
        
    except Exception as e:
        return False, f"Database validation failed: {str(e)}"

# Initialize database when module is imported
if __name__ == "__main__":
    setup_database()
else:
    # Only setup if database doesn't exist
    if not os.path.exists('rental_management.db'):
        setup_database()