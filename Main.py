import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import os
from datetime import datetime

def connect():
    return sqlite3.connect('rental_management.db')

def setup_database():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS properties (
        property_id INTEGER PRIMARY KEY,
        property_name TEXT NOT NULL,
        location TEXT NOT NULL,
        rent_amount REAL NOT NULL,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tenants (
        tenant_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS leases (
        lease_id INTEGER PRIMARY KEY,
        property_id INTEGER NOT NULL,
        tenant_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        status TEXT DEFAULT 'Active',
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY,
        lease_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        payment_date TEXT NOT NULL,
        payment_method TEXT DEFAULT 'Cash',
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')


    conn.commit()
    conn.close()

setup_database()

ADMIN_EMAIL = "groupj@python.com"
ADMIN_PASSWORD = "groupj"
current_user = None
user_type = None

class UbuntuRentalApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rental Management System - Group J")
        self.root.geometry("700x500")
        self.root.configure(bg='#f0f0f0')
        self.setup_login()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def add_spacer(self, parent, height=10):
        tk.Label(parent, text="", height=height//8, bg=parent.cget('bg')).pack()
    
    def setup_login(self):
        self.clear_window()
        self.root.title("Login - Rental Management System")
        self.root.geometry("500x450")
        
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        header_frame = tk.Frame(main_frame, bg='#2c5aa0', relief='raised', bd=2)
        header_frame.pack(fill='x')
        
        title_label = tk.Label(header_frame, text="RENTAL MANAGEMENT SYSTEM", 
                              bg='#2c5aa0', fg='white', pady=15)
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Group J - BSD 2302 Python Programming", 
                                 bg='#2c5aa0', fg='white', pady=15)
        subtitle_label.pack()
        
        self.add_spacer(main_frame, 20)
        
        # Login form
        form_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        form_frame.pack(fill='x', pady=10, padx=20)
        
        tk.Label(form_frame, text="USER LOGIN", bg='white', pady=15).pack()
        
        # Email field
        tk.Label(form_frame, text="Email Address:", bg='white', anchor='w').pack(fill='x', padx=20)
        self.email_entry = tk.Entry(form_frame, width=40, relief='sunken', bd=2)
        self.email_entry.pack(pady=5, padx=20)
        
        self.add_spacer(form_frame, 10)
        
        # Password field
        tk.Label(form_frame, text="Password:", bg='white', anchor='w').pack(fill='x', padx=20)
        self.password_entry = tk.Entry(form_frame, width=40, show="*", relief='sunken', bd=2)
        self.password_entry.pack(pady=5, padx=20)
        
        # Login button
        login_btn = tk.Button(form_frame, text="LOGIN", command=self.login, 
                             bg='#28a745', fg='white', width=15, pady=5)
        login_btn.pack(pady=20)
        
        # Credentials info
        info_frame = tk.Frame(main_frame, bg='#f8f9fa', relief='raised', bd=1)
        info_frame.pack(fill='x', pady=10, padx=20)
        
        tk.Label(info_frame, text="TEST CREDENTIALS", bg='#f8f9fa', pady=10).pack()
        tk.Label(info_frame, text="Username: groupj@python.com /Password: groupj", bg='#f8f9fa').pack()
        
        # Bind Enter key
        self.email_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.bind('<Return>', lambda e: self.login())
        self.email_entry.focus()
    
    def login(self):
        global current_user, user_type
        
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
        
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            current_user = "Admin"
            user_type = "Admin"
            self.setup_admin_dashboard()
        else:
            try:
                conn = connect()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tenants WHERE email = ? AND password = ?", (email, password))
                tenant = cursor.fetchone()
                conn.close()
                
                if tenant:
                    current_user = tenant
                    user_type = "Tenant"
                    self.setup_tenant_dashboard()
                else:
                    messagebox.showerror("Login Failed", "Invalid email or password")
            except Exception as e:
                messagebox.showerror("Error", f"Login error: {str(e)}")
    
    def setup_admin_dashboard(self):
        self.clear_window()
        self.root.title("Admin Dashboard - Rental Management System")
        self.root.geometry("900x700")
        
        header_frame = tk.Frame(self.root, bg='#2c5aa0', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="ADMIN DASHBOARD", bg='#2c5aa0', fg='white', pady=20).pack()
        tk.Label(header_frame, text="Rental System Management", bg='#2c5aa0', fg='white').pack()
        
        content_frame = tk.Frame(self.root, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.show_admin_stats(content_frame)
        
        self.show_admin_menu(content_frame)
        
        footer_frame = tk.Frame(self.root, bg='#343a40', height=50)
        footer_frame.pack(fill='x')
        footer_frame.pack_propagate(False)
        
        logout_btn = tk.Button(footer_frame, text="LOGOUT", command=self.logout, 
                              bg='#dc3545', fg='white', width=10)
        logout_btn.pack(side='right', padx=20, pady=10)
        
        tk.Label(footer_frame, text="Logged in as Administrator", bg='#343a40', fg='white').pack(side='left', padx=20, pady=15)
    
    def show_admin_stats(self, parent):
        try:
            conn = connect()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM properties")
            total_properties = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tenants")
            total_tenants = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM leases WHERE status = 'Active'")
            active_leases = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(amount) FROM payments")
            total_payments = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT COUNT(*) FROM payments WHERE date(payment_date) >= date('now', 'start of month')")
            monthly_payments = cursor.fetchone()[0]
            
            conn.close()
            
            stats_frame = tk.LabelFrame(parent, text="SYSTEM STATISTICS", bg='white', relief='raised', bd=2)
            stats_frame.pack(fill='x')
            
            self.add_spacer(stats_frame, 20)
            
            grid_frame = tk.Frame(stats_frame, bg='white')
            grid_frame.pack(fill='x', padx=20, pady=15)
            
            self.create_stat_box(grid_frame, "PROPERTIES", total_properties, 0, 0)
            self.create_stat_box(grid_frame, "TENANTS", total_tenants, 0, 1)
            self.create_stat_box(grid_frame, "ACTIVE LEASES", active_leases, 0, 2)
            
            self.create_stat_box(grid_frame, "TOTAL REVENUE", f"KES{total_payments:.2f}", 1, 0)
            self.create_stat_box(grid_frame, "MONTHLY PAYMENTS", f"KES{monthly_payments:.2f}", 1, 1)
            self.create_stat_box(grid_frame, "SYSTEM STATUS", "OPERATIONAL", 1, 2)
            
            for i in range(3):
                grid_frame.columnconfigure(i, weight=1)
                
            self.add_spacer(stats_frame, 20)
            
        except Exception as e:
            error_label = tk.Label(parent, text=f"Error loading statistics: {str(e)}", bg='#f8d7da', fg='#721c24')
            error_label.pack(fill='x', padx=20, pady=10)
    
    def create_stat_box(self, parent, label, value, row, col):
        stat_frame = tk.Frame(parent, bg='#f8f9fa', relief='raised', bd=1)
        stat_frame.grid(row=row, column=col, padx=10, pady=5, sticky='ew')
        
        tk.Label(stat_frame, text=str(value), bg='#f8f9fa', fg='#2c5aa0', pady=5).pack()
        tk.Label(stat_frame, text=label, bg='#f8f9fa', fg='#6c757d', pady=5).pack()
    
    def show_admin_menu(self, parent):
        self.add_spacer(parent, 20)
        
        menu_frame = tk.LabelFrame(parent, text="ADMINISTRATIVE FUNCTIONS", bg='white', relief='raised', bd=2)
        menu_frame.pack(fill='both', expand=True)
        
        grid_frame = tk.Frame(menu_frame, bg='white')
        grid_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        buttons = [
            ("ADD PROPERTY", "Add new rental properties", self.add_property, '#28a745'),
            ("REGISTER TENANT", "Register new tenants", self.register_tenant, '#17a2b8'),
            ("ASSIGN LEASE", "Create lease agreements", self.assign_lease, '#ffc107'),
            ("RECORD PAYMENT", "Record rent payments", self.record_payment, '#fd7e14'),
            ("VIEW REPORTS", "System reports & analytics", self.view_reports, '#6f42c1'),
            ("LIST ALL DATA", "View all system data", self.list_all_data, '#20c997')
        ]
        
        for i, (text, desc, command, color) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            btn_frame = tk.Frame(grid_frame, bg='white', relief='raised', bd=1)
            btn_frame.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            
            tk.Button(btn_frame, text=text, command=command, bg=color, fg='white', 
                     width=20, pady=10).pack(padx=10, pady=10)
            tk.Label(btn_frame, text=desc, bg='white', fg='#6c757d', wraplength=150).pack(pady=10)
        
        for i in range(3):
            grid_frame.columnconfigure(i, weight=1)
    
    def setup_tenant_dashboard(self):
        self.clear_window()
        self.root.title("Tenant Dashboard - Rental Management System")
        self.root.geometry("700x600")
        
        header_frame = tk.Frame(self.root, bg='#28a745', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="TENANT PORTAL", bg='#28a745', fg='white', pady=15).pack()
        if current_user:
            tk.Label(header_frame, text=f"Welcome, {current_user[1]}!", bg='#28a745', fg='white').pack()
        
        content_frame = tk.Frame(self.root, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.show_tenant_info(content_frame)
        
        menu_frame = tk.LabelFrame(content_frame, text="TENANT SERVICES", bg='white', relief='raised', bd=2)
        menu_frame.pack(fill='x', pady=20)
        
        btn_frame = tk.Frame(menu_frame, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="VIEW MY LEASES", command=self.view_my_leases, 
                 bg='#17a2b8', fg='white', width=20, pady=10).pack(pady=5)
        tk.Button(btn_frame, text="PAYMENT HISTORY", command=self.view_my_payments, 
                 bg='#28a745', fg='white', width=20, pady=10).pack(pady=5)
        
        footer_frame = tk.Frame(self.root, bg='#343a40', height=50)
        footer_frame.pack(fill='x')
        footer_frame.pack_propagate(False)
        
        logout_btn = tk.Button(footer_frame, text="LOGOUT", command=self.logout, 
                              bg='#dc3545', fg='white', width=10)
        logout_btn.pack(side='right', padx=20, pady=10)
        
        tk.Label(footer_frame, text=f"Logged in as {current_user[1]}", bg='#343a40', fg='white').pack(side='left', padx=20, pady=15)
    
    def show_tenant_info(self, parent):
        try:
            if current_user:
                conn = connect()
                cursor = conn.cursor()
                
                # Get tenant statistics
                cursor.execute("SELECT COUNT(*) FROM leases WHERE tenant_id = ? AND status = 'Active'", (current_user[0],))
                active_leases = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT COUNT(*), SUM(amount) 
                    FROM payments p
                    JOIN leases l ON p.lease_id = l.lease_id
                    WHERE l.tenant_id = ?
                """, (current_user[0],))
                payment_info = cursor.fetchone()
                
                cursor.execute("""
                    SELECT MAX(payment_date)
                    FROM payments p
                    JOIN leases l ON p.lease_id = l.lease_id
                    WHERE l.tenant_id = ?
                """, (current_user[0],))
                last_payment = cursor.fetchone()[0]
                
                conn.close()
                
                info_frame = tk.LabelFrame(parent, text="ACCOUNT SUMMARY", bg='white', relief='raised', bd=2)
                info_frame.pack(fill='x')
                
                self.add_spacer(info_frame, 20)
                
                grid_frame = tk.Frame(info_frame, bg='white')
                grid_frame.pack(fill='x', padx=20, pady=15)
                
                self.create_stat_box(grid_frame, "ACTIVE LEASES", active_leases, 0, 0)
                self.create_stat_box(grid_frame, "TOTAL PAYMENTS", payment_info[0] if payment_info else 0, 0, 1)
                self.create_stat_box(grid_frame, "AMOUNT PAID", f"KES{payment_info[1]:.2f}" if payment_info and payment_info[1] else "KES0.00", 1, 0)
                self.create_stat_box(grid_frame, "LAST PAYMENT", last_payment if last_payment else "None", 1, 1)
                
                for i in range(2):
                    grid_frame.columnconfigure(i, weight=1)
                
                self.add_spacer(info_frame, 20)
                
        except Exception as e:
            error_label = tk.Label(parent, text=f"Error loading account info: {str(e)}", bg='#f8d7da', fg='#721c24')
            error_label.pack(fill='x', padx=20, pady=10)
    
    def add_property(self):
        """Add new property using simple dialogs"""
        try:
            prop_id = simpledialog.askstring("Add Property", "Enter Property ID:")
            if not prop_id:
                return
            
            prop_name = simpledialog.askstring("Add Property", "Enter Property Name:")
            if not prop_name:
                return
            
            location = simpledialog.askstring("Add Property", "Enter Location:")
            if not location:
                return
            
            rent = simpledialog.askstring("Add Property", "Enter Monthly Rent Amount:")
            if not rent:
                return
            
            conn = connect()
            cursor = conn.cursor()
            
            cursor.execute("SELECT property_id FROM properties WHERE property_id = ?", (int(prop_id),))
            if cursor.fetchone():
                messagebox.showerror("Error", "Property ID already exists!")
                conn.close()
                return
            
            cursor.execute("INSERT INTO properties (property_id, property_name, location, rent_amount) VALUES (?, ?, ?, ?)",
                         (int(prop_id), prop_name, location, float(rent)))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Property '{prop_name}' added successfully!")
            self.setup_admin_dashboard()  
            
        except ValueError:
            messagebox.showerror("Error", "Property ID must be a number and rent must be a valid amount!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add property: {str(e)}")
    
    def register_tenant(self):
        try:
            tenant_id = simpledialog.askstring("Register Tenant", "Enter Tenant ID:")
            if not tenant_id:
                return
            
            name = simpledialog.askstring("Register Tenant", "Enter Full Name:")
            if not name:
                return
            
            email = simpledialog.askstring("Register Tenant", "Enter Email Address:")
            if not email:
                return
            
            if "@" not in email:
                messagebox.showerror("Error", "Please enter a valid email address!")
                return
            
            password = simpledialog.askstring("Register Tenant", "Enter Password:")
            if not password:
                return
            
            conn = connect()
            cursor = conn.cursor()
            
            cursor.execute("SELECT tenant_id FROM tenants WHERE tenant_id = ? OR email = ?", 
                         (int(tenant_id), email))
            if cursor.fetchone():
                messagebox.showerror("Error", "Tenant ID or email already exists!")
                conn.close()
                return
            
            cursor.execute("INSERT INTO tenants (tenant_id, name, email, password) VALUES (?, ?, ?, ?)",
                         (int(tenant_id), name, email, password))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Tenant '{name}' registered successfully!")
            self.setup_admin_dashboard()  
            
        except ValueError:
            messagebox.showerror("Error", "Tenant ID must be a number!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register tenant: {str(e)}")
    
    def assign_lease(self):
        try:
            conn = connect()
            cursor = conn.cursor()
            
            cursor.execute("SELECT property_id, property_name, location FROM properties")
            properties = cursor.fetchall()
            
            cursor.execute("SELECT tenant_id, name, email FROM tenants")
            tenants = cursor.fetchall()
            
            conn.close()
            
            if not properties:
                messagebox.showerror("Error", "No properties available! Add properties first.")
                return
            
            if not tenants:
                messagebox.showerror("Error", "No tenants available! Register tenants first.")
                return
            
            lease_id = simpledialog.askstring("Lease Assignment", "Enter Lease ID:")
            if not lease_id:
                return
            
            property_list = [f"{p[0]} - {p[1]} ({p[2]})" for p in properties]
            property_choice = self.show_selection_dialog("Select Property", property_list)
            if property_choice is None:
                return
            property_id = properties[property_choice][0]
            
            tenant_list = [f"{t[0]} - {t[1]} ({t[2]})" for t in tenants]
            tenant_choice = self.show_selection_dialog("Select Tenant", tenant_list)
            if tenant_choice is None:
                return
            tenant_id = tenants[tenant_choice][0]
            
            start_date = simpledialog.askstring("Lease Assignment", "Enter Start Date (YYYY-MM-DD):")
            if not start_date:
                return
            
            end_date = simpledialog.askstring("Lease Assignment", "Enter End Date (YYYY-MM-DD):")
            if not end_date:
                return
            
            conn = connect()
            cursor = conn.cursor()
            
            cursor.execute("SELECT lease_id FROM leases WHERE lease_id = ?", (int(lease_id),))
            if cursor.fetchone():
                messagebox.showerror("Error", "Lease ID already exists!")
                conn.close()
                return
            
            cursor.execute("INSERT INTO leases (lease_id, property_id, tenant_id, start_date, end_date, status) VALUES (?, ?, ?, ?, ?, ?)",
                         (int(lease_id), property_id, tenant_id, start_date, end_date, 'Active'))
            conn.commit()
            conn.close()
            
            property_name = properties[property_choice][1]
            tenant_name = tenants[tenant_choice][1]
            messagebox.showinfo("Success", f"Lease assigned successfully!\n\nProperty: {property_name}\nTenant: {tenant_name}\nPeriod: {start_date} to {end_date}")
            self.setup_admin_dashboard()  
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to assign lease: {str(e)}")
    
    def show_selection_dialog(self, title, options):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("400x300")
        window.grab_set()
        
        selected_index = tk.IntVar()
        selected_index.set(-1)
        
        tk.Label(window, text=title, pady=10).pack()
        
        frame = tk.Frame(window)
        frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
        for option in options:
            listbox.insert(tk.END, option)
        listbox.pack(fill='both', expand=True)
        scrollbar.config(command=listbox.yview)
        
        def on_select():
            selection = listbox.curselection()
            if selection:
                selected_index.set(selection[0])
                window.destroy()
            else:
                messagebox.showerror("Error", "Please select an option!")
        
        def on_cancel():
            selected_index.set(-1)
            window.destroy()
        
        button_frame = tk.Frame(window)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="SELECT", command=on_select, bg='#28a745', fg='white').pack(side='left', padx=5)
        tk.Button(button_frame, text="CANCEL", command=on_cancel, bg='#6c757d', fg='white').pack(side='left', padx=5)
        
        window.wait_window()
        
        return selected_index.get() if selected_index.get() >= 0 else None
    
    def record_payment(self):
        """Record payment with lease selection"""
        try:
            conn = connect()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT l.lease_id, p.property_name, t.name, p.rent_amount
                FROM leases l 
                JOIN properties p ON l.property_id = p.property_id 
                JOIN tenants t ON l.tenant_id = t.tenant_id
                WHERE l.status = 'Active'
            """)
            leases = cursor.fetchall()
            conn.close()
            
            if not leases:
                messagebox.showerror("Error", "No active leases available!")
                return
            
            payment_id = simpledialog.askstring("Record Payment", "Enter Payment ID:")
            if not payment_id:
                return
            
            lease_list = [f"Lease {l[0]} - {l[1]} ({l[2]}) - KSH {l[3]:.2f}" for l in leases]
            lease_choice = self.show_selection_dialog("Select Lease", lease_list)
            if lease_choice is None:
                return
            lease_id = leases[lease_choice][0]
            
            amount = simpledialog.askstring("Record Payment", "Enter Payment Amount:")
            if not amount:
                return
            
            payment_date = simpledialog.askstring("Record Payment", "Enter Payment Date (YYYY-MM-DD):")
            if not payment_date:
                return
            
            methods = ["Cash", "Bank Transfer", "Mobile Money", "Cheque"]
            method_choice = self.show_selection_dialog("Select Payment Method", methods)
            payment_method = methods[method_choice] if method_choice is not None else "Cash"
            
            conn = connect()
            cursor = conn.cursor()
            
            cursor.execute("SELECT payment_id FROM payments WHERE payment_id = ?", (int(payment_id),))
            if cursor.fetchone():
                messagebox.showerror("Error", "Payment ID already exists!")
                conn.close()
                return
            
            cursor.execute("INSERT INTO payments (payment_id, lease_id, amount, payment_date, payment_method) VALUES (?, ?, ?, ?, ?)",
                         (int(payment_id), lease_id, float(amount), payment_date, payment_method))
            conn.commit()
            conn.close()
            
            lease_info = leases[lease_choice]
            messagebox.showinfo("Success", f"Payment recorded successfully!\n\nAmount: KSH {float(amount):.2f}\nProperty: {lease_info[1]}\nTenant: {lease_info[2]}\nMethod: {payment_method}")
            self.setup_admin_dashboard() 
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to record payment: {str(e)}")
    
    def view_reports(self):
        window = tk.Toplevel(self.root)
        window.title("System Reports & Analysis")
        window.geometry("800x600")
        window.configure(bg='#f0f0f0')
        
        header_frame = tk.Frame(window, bg='#6f42c1')
        header_frame.pack(fill='x')
        tk.Label(header_frame, text="SYSTEM REPORTS & ANALYTICS", bg='#6f42c1', fg='white', pady=15).pack()
        
        try:
            conn = connect()
            cursor = conn.cursor()
            
            content_frame = tk.Frame(window, bg='#f0f0f0')
            content_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            stats_frame = tk.LabelFrame(content_frame, text="SUMMARY STATISTICS", bg='white', relief='raised', bd=2)
            stats_frame.pack(fill='x', pady=15)
            
            cursor.execute("SELECT COUNT(*) FROM properties")
            total_properties = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tenants")
            total_tenants = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM leases")
            total_leases = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM leases WHERE status = 'Active'")
            active_leases = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*), SUM(amount) FROM payments")
            payment_data = cursor.fetchone()
            total_payment_count = payment_data[0]
            total_revenue = payment_data[1] or 0
            
            cursor.execute("SELECT AVG(rent_amount) FROM properties")
            avg_rent = cursor.fetchone()[0] or 0
            
            stats_text = tk.Text(stats_frame, height=8, bg='white')
            stats_text.pack(fill='x', padx=10, pady=10)
            
            stats_text.insert(tk.END, f"RENTAL MANAGEMENT SYSTEM - REPORT\n")
            stats_text.insert(tk.END, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            stats_text.insert(tk.END, f"PROPERTY STATISTICS:\n")
            stats_text.insert(tk.END, f"  Total Properties: {total_properties}\n")
            stats_text.insert(tk.END, f"  Average Monthly Rent: KSH {avg_rent:.2f}\n\n")
            stats_text.insert(tk.END, f"TENANT & LEASE STATISTICS:\n")
            stats_text.insert(tk.END, f"  Total Tenants: {total_tenants}\n")
            stats_text.insert(tk.END, f"  Total Leases: {total_leases}\n")
            stats_text.insert(tk.END, f"  Active Leases: {active_leases}\n")
            stats_text.insert(tk.END, f"  Occupancy Rate: {(active_leases/total_properties*100) if total_properties > 0 else 0:.1f}%\n\n")
            stats_text.insert(tk.END, f"FINANCIAL STATISTICS:\n")
            stats_text.insert(tk.END, f"  Total Payments Recorded: {total_payment_count}\n")
            stats_text.insert(tk.END, f"  Total Revenue: KSH {total_revenue:.2f}\n")
            stats_text.insert(tk.END, f"  Average Payment: KSH {(total_revenue/total_payment_count) if total_payment_count > 0 else 0:.2f}\n")
            
            activities_frame = tk.LabelFrame(content_frame, text="RECENT ACTIVITIES", bg='white', relief='raised', bd=2)
            activities_frame.pack(fill='both', expand=True)
            
            text_widget = tk.Text(activities_frame, height=15, bg='white')
            scrollbar = tk.Scrollbar(activities_frame, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side='left', fill='both', expand=True, padx=10, pady=10)
            scrollbar.pack(side='right', fill='y', pady=10)
            
            text_widget.insert(tk.END, "RECENT PAYMENTS:\n" + "="*50 + "\n")
            cursor.execute("""
                SELECT p.payment_id, p.amount, p.payment_date, p.payment_method, t.name, pr.property_name
                FROM payments p
                JOIN leases l ON p.lease_id = l.lease_id
                JOIN tenants t ON l.tenant_id = t.tenant_id
                JOIN properties pr ON l.property_id = pr.property_id
                ORDER BY p.payment_date DESC, p.payment_id DESC
                LIMIT 15
            """)
            recent_payments = cursor.fetchall()
            
            for payment in recent_payments:
                text_widget.insert(tk.END, f"Payment #{payment[0]}: KSH {payment[1]:.2f} by {payment[4]}\n")
                text_widget.insert(tk.END, f"  Property: {payment[5]}\n")
                text_widget.insert(tk.END, f"  Date: {payment[2]} | Method: {payment[3]}\n\n")
            
            text_widget.insert(tk.END, "\nPROPERTY PERFORMANCE:\n" + "="*50 + "\n")
            cursor.execute("""
                SELECT p.property_name, p.rent_amount, COUNT(l.lease_id) as lease_count,
                       COALESCE(SUM(pay.amount), 0) as total_revenue
                FROM properties p
                LEFT JOIN leases l ON p.property_id = l.property_id
                LEFT JOIN payments pay ON l.lease_id = pay.lease_id
                GROUP BY p.property_id, p.property_name, p.rent_amount
                ORDER BY total_revenue DESC
            """)
            property_performance = cursor.fetchall()
            
            for prop in property_performance:
                text_widget.insert(tk.END, f"{prop[0]}:\n")
                text_widget.insert(tk.END, f"  Monthly Rent: KSH {prop[1]:.2f}\n")
                text_widget.insert(tk.END, f"  Total Leases: {prop[2]}\n")
                text_widget.insert(tk.END, f"  Revenue Generated: KSH {prop[3]:.2f}\n\n")
            
            conn.close()
            
        except Exception as e:
            error_label = tk.Label(window, text=f"Error generating reports: {str(e)}", bg='#f8d7da', fg='#721c24')
            error_label.pack(pady=20)
        
        tk.Button(window, text="CLOSE", command=window.destroy, bg='#6c757d', fg='white', width=15).pack(pady=10)
    
    def list_all_data(self):
        """Show all system data in organized format"""
        window = tk.Toplevel(self.root)
        window.title("System Data")
        window.geometry("900x700")
        window.configure(bg='#f0f0f0')
        
        header_frame = tk.Frame(window, bg='#20c997')
        header_frame.pack(fill='x')
        tk.Label(header_frame, text="SYSTEM DATA", bg='#20c997', fg='white', pady=15).pack()
        
        content_frame = tk.Frame(window, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tab_frame = tk.Frame(content_frame, bg='#f0f0f0')
        tab_frame.pack(fill='x', pady=10)
        
        text_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=2)
        text_frame.pack(fill='both', expand=True)
        
        text_widget = tk.Text(text_frame, height=30, bg='white')
        scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        def show_properties():
            text_widget.delete(1.0, tk.END)
            try:
                conn = connect()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM properties ORDER BY property_id")
                properties = cursor.fetchall()
                conn.close()
                
                text_widget.insert(tk.END, "ALL PROPERTIES\n" + "="*60 + "\n\n")
                for prop in properties:
                    text_widget.insert(tk.END, f"Property ID: {prop[0]}\n")
                    text_widget.insert(tk.END, f"Name: {prop[1]}\n")
                    text_widget.insert(tk.END, f"Location: {prop[2]}\n")
                    text_widget.insert(tk.END, f"Monthly Rent: KSH {prop[3]:.2f}\n")
                    text_widget.insert(tk.END, f"Created: {prop[4] if len(prop) > 4 else 'N/A'}\n")
                    text_widget.insert(tk.END, "-" * 40 + "\n\n")
            except Exception as e:
                text_widget.insert(tk.END, f"Error loading properties: {str(e)}")
        
        def show_tenants():
            text_widget.delete(1.0, tk.END)
            try:
                conn = connect()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tenants ORDER BY tenant_id")
                tenants = cursor.fetchall()
                conn.close()
                
                text_widget.insert(tk.END, "ALL TENANTS\n" + "="*60 + "\n\n")
                for tenant in tenants:
                    text_widget.insert(tk.END, f"Tenant ID: {tenant[0]}\n")
                    text_widget.insert(tk.END, f"Name: {tenant[1]}\n")
                    text_widget.insert(tk.END, f"Email: {tenant[2]}\n")
                    text_widget.insert(tk.END, f"Password: {'*' * len(tenant[3])}\n")
                    text_widget.insert(tk.END, f"Created: {tenant[4] if len(tenant) > 4 else 'N/A'}\n")
                    text_widget.insert(tk.END, "-" * 40 + "\n\n")
            except Exception as e:
                text_widget.insert(tk.END, f"Error loading tenants: {str(e)}")
        
        def show_leases():
            text_widget.delete(1.0, tk.END)
            try:
                conn = connect()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT l.*, p.property_name, t.name
                    FROM leases l
                    JOIN properties p ON l.property_id = p.property_id
                    JOIN tenants t ON l.tenant_id = t.tenant_id
                    ORDER BY l.lease_id
                """)
                leases = cursor.fetchall()
                conn.close()
                
                text_widget.insert(tk.END, "ALL LEASES\n" + "="*60 + "\n\n")
                for lease in leases:
                    text_widget.insert(tk.END, f"Lease ID: {lease[0]}\n")
                    text_widget.insert(tk.END, f"Property: {lease[7]} (ID: {lease[1]})\n")
                    text_widget.insert(tk.END, f"Tenant: {lease[8]} (ID: {lease[2]})\n")
                    text_widget.insert(tk.END, f"Period: {lease[3]} to {lease[4]}\n")
                    text_widget.insert(tk.END, f"Status: {lease[5] if len(lease) > 5 else 'Active'}\n")
                    text_widget.insert(tk.END, f"Created: {lease[6] if len(lease) > 6 else 'N/A'}\n")
                    text_widget.insert(tk.END, "-" * 40 + "\n\n")
            except Exception as e:
                text_widget.insert(tk.END, f"Error loading leases: {str(e)}")
        
        def show_payments():
            text_widget.delete(1.0, tk.END)
            try:
                conn = connect()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT p.*, l.lease_id, pr.property_name, t.name
                    FROM payments p
                    JOIN leases l ON p.lease_id = l.lease_id
                    JOIN properties pr ON l.property_id = pr.property_id
                    JOIN tenants t ON l.tenant_id = t.tenant_id
                    ORDER BY p.payment_date DESC, p.payment_id
                """)
                payments = cursor.fetchall()
                conn.close()
                
                text_widget.insert(tk.END, "ALL PAYMENTS\n" + "="*60 + "\n\n")
                for payment in payments:
                    text_widget.insert(tk.END, f"Payment ID: {payment[0]}\n")
                    text_widget.insert(tk.END, f"Amount: KSH {payment[2]:.2f}\n")
                    text_widget.insert(tk.END, f"Date: {payment[3]}\n")
                    text_widget.insert(tk.END, f"Method: {payment[4] if len(payment) > 4 else 'Not specified'}\n")
                    text_widget.insert(tk.END, f"Lease: {payment[1]}\n")
                    text_widget.insert(tk.END, f"Property: {payment[7]}\n")
                    text_widget.insert(tk.END, f"Tenant: {payment[8]}\n")
                    text_widget.insert(tk.END, f"Created: {payment[5] if len(payment) > 5 else 'N/A'}\n")
                    text_widget.insert(tk.END, "-" * 40 + "\n\n")
            except Exception as e:
                text_widget.insert(tk.END, f"Error loading payments: {str(e)}")
        
        tk.Button(tab_frame, text="PROPERTIES", command=show_properties, bg='#28a745', fg='white', width=12).pack(side='left', padx=2)
        tk.Button(tab_frame, text="TENANTS", command=show_tenants, bg='#17a2b8', fg='white', width=12).pack(side='left', padx=2)
        tk.Button(tab_frame, text="LEASES", command=show_leases, bg='#ffc107', fg='black', width=12).pack(side='left', padx=2)
        tk.Button(tab_frame, text="PAYMENTS", command=show_payments, bg='#fd7e14', fg='white', width=12).pack(side='left', padx=2)
        
        show_properties()
        
        tk.Button(window, text="CLOSE", command=window.destroy, bg='#6c757d', fg='white', width=15).pack(pady=10)
    
    def view_my_leases(self):
        """Show tenant's leases and payments"""
        window = tk.Toplevel(self.root)
        window.title("My Leases and Payments")
        window.geometry("800x600")
        window.configure(bg='#f0f0f0')
        
        header_frame = tk.Frame(window, bg='#17a2b8')
        header_frame.pack(fill='x')
        tk.Label(header_frame, text="MY LEASES AND PAYMENTS", bg='#17a2b8', fg='white', pady=15).pack()
        
        try:
            conn = connect()
            cursor = conn.cursor()
            
            content_frame = tk.Frame(window, bg='white', relief='raised', bd=2)
            content_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            text_widget = tk.Text(content_frame, height=25, bg='white')
            scrollbar = tk.Scrollbar(content_frame, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side='left', fill='both', expand=True, padx=10, pady=10)
            scrollbar.pack(side='right', fill='y', pady=10)
            
            cursor.execute("""
                SELECT l.lease_id, p.property_name, p.location, l.start_date, l.end_date, p.rent_amount, l.status
                FROM leases l
                JOIN properties p ON l.property_id = p.property_id
                WHERE l.tenant_id = ?
                ORDER BY l.start_date DESC
            """, (current_user[0],))
            leases = cursor.fetchall()
            
            if not leases:
                text_widget.insert(tk.END, "No leases found for your account.\n")
            else:
                text_widget.insert(tk.END, f"LEASE INFORMATION FOR {current_user[1]}\n")
                text_widget.insert(tk.END, "="*60 + "\n\n")
                
                for lease in leases:
                    text_widget.insert(tk.END, f"LEASE #{lease[0]}\n")
                    text_widget.insert(tk.END, f"Property: {lease[1]}\n")
                    text_widget.insert(tk.END, f"Location: {lease[2]}\n")
                    text_widget.insert(tk.END, f"Lease Period: {lease[3]} to {lease[4]}\n")
                    text_widget.insert(tk.END, f"Monthly Rent: KSH {lease[5]:.2f}\n")
                    text_widget.insert(tk.END, f"Status: {lease[6]}\n\n")
                    
                    cursor.execute("""
                        SELECT payment_id, amount, payment_date, payment_method 
                        FROM payments 
                        WHERE lease_id = ? 
                        ORDER BY payment_date DESC
                    """, (lease[0],))
                    payments = cursor.fetchall()
                    
                    text_widget.insert(tk.END, "PAYMENT HISTORY:\n")
                    if payments:
                        total_paid = sum(p[1] for p in payments)
                        text_widget.insert(tk.END, f"Total Payments Made: {len(payments)}\n")
                        text_widget.insert(tk.END, f"Total Amount Paid: KSH {total_paid:.2f}\n\n")
                        
                        for payment in payments:
                            text_widget.insert(tk.END, f"  Payment #{payment[0]}: KSH {payment[1]:.2f}\n")
                            text_widget.insert(tk.END, f"  Date: {payment[2]} | Method: {payment[3]}\n\n")
                    else:
                        text_widget.insert(tk.END, "  No payments recorded for this lease.\n\n")
                    
                    text_widget.insert(tk.END, "="*60 + "\n\n")
            
            conn.close()
            
        except Exception as e:
            text_widget.insert(tk.END, f"Error loading lease information: {str(e)}\n")
        
        tk.Button(window, text="CLOSE", command=window.destroy, bg='#6c757d', fg='white', width=15).pack(pady=10)
    
    def view_my_payments(self):
        """Show tenant's payment history only"""
        window = tk.Toplevel(self.root)
        window.title("My Payment History")
        window.geometry("700x500")
        window.configure(bg='#f0f0f0')
        
        header_frame = tk.Frame(window, bg='#28a745')
        header_frame.pack(fill='x')
        tk.Label(header_frame, text="MY PAYMENT HISTORY", bg='#28a745', fg='white', pady=15).pack()
        
        try:
            conn = connect()
            cursor = conn.cursor()
            
            content_frame = tk.Frame(window, bg='white', relief='raised', bd=2)
            content_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            text_widget = tk.Text(content_frame, height=20, bg='white')
            scrollbar = tk.Scrollbar(content_frame, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side='left', fill='both', expand=True, padx=10, pady=10)
            scrollbar.pack(side='right', fill='y', pady=10)
            
            cursor.execute("""
                SELECT p.payment_id, p.amount, p.payment_date, p.payment_method, pr.property_name
                FROM payments p
                JOIN leases l ON p.lease_id = l.lease_id
                JOIN properties pr ON l.property_id = pr.property_id
                WHERE l.tenant_id = ?
                ORDER BY p.payment_date DESC
            """, (current_user[0],))
            payments = cursor.fetchall()
            
            if not payments:
                text_widget.insert(tk.END, "No payment history found.\n")
            else:
                total_amount = sum(p[1] for p in payments)
                text_widget.insert(tk.END, f"PAYMENT HISTORY FOR {current_user[1]}\n")
                text_widget.insert(tk.END, "="*50 + "\n\n")
                text_widget.insert(tk.END, f"Total Payments Made: {len(payments)}\n")
                text_widget.insert(tk.END, f"Total Amount Paid: KSH {total_amount:.2f}\n\n")
                text_widget.insert(tk.END, "PAYMENT DETAILS:\n")
                text_widget.insert(tk.END, "-" * 50 + "\n\n")
                
                for payment in payments:
                    text_widget.insert(tk.END, f"Payment #{payment[0]}\n")
                    text_widget.insert(tk.END, f"Amount: KSH {payment[1]:.2f}\n")
                    text_widget.insert(tk.END, f"Date: {payment[2]}\n")
                    text_widget.insert(tk.END, f"Method: {payment[3]}\n")
                    text_widget.insert(tk.END, f"Property: {payment[4]}\n\n")
            
            conn.close()
            
        except Exception as e:
            text_widget.insert(tk.END, f"Error loading payment history: {str(e)}\n")
        
        tk.Button(window, text="CLOSE", command=window.destroy, bg='#6c757d', fg='white', width=15).pack(pady=10)
    
    def logout(self):
        global current_user, user_type
        current_user = None
        user_type = None
        self.setup_login()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = UbuntuRentalApp()
    app.run()