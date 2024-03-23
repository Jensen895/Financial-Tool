import tkinter as tk
import sqlite3
from datetime import datetime

from AddEmployeeForm import AddEmployeeForm
from ListEmployeeForm import ListEmployeeForm
from AddCustomerForm import AddCustomerForm
from ListCustomersForm import ListCustomersForm
from AddVendorForm import AddVendorForm
from ListVendorsForm import ListVendorsForm
from ShowBalanceSheet import ShowBalanceSheet
from ShowIncomeStatement import ShowIncomeStatement
from PayEmployee import PayEmployee
from ListPayroll import ListPayroll
from LIstInventory import ListInventory
from CreateInvoice import CreateInvoice
from CreatePO import CreatePO

class EmployeeAppMenu:
    def __init__(self, master):
        self.federal_tax_withold = 0.1175
        self.state_tax_withold = 0.0495
        self.medicare_withold = 0.0145
        self.ssn_withold = 0.06
        self.payroll_withold = self.federal_tax_withold + self.state_tax_withold + self.medicare_withold + self.ssn_withold 
        
        self.master = master
        self.master.title("ENG566 Computer Program")

        self.connection = sqlite3.connect("final_database.db")
        self.cursor = self.connection.cursor()
        
        # Create a table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                             (first_name TEXT, last_name TEXT, address1 TEXT, address2 TEXT, city TEXT, state TEXT, zipcode INTEGER, ssn INTEGER PRIMARY KEY, witholdings REAL, salary REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS customers
                             (company_name TEXT PRIMARY KEY, last_name TEXT, first_name TEXT, address1 TEXT, city TEXT, state TEXT, zipcode INTEGER, price REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS vendors
                             (company_name TEXT PRIMARY KEY, part TEXT, price REAL, address1 TEXT, address2 TEXT, city TEXT, state TEXT, zipcode INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS balance_sheet
                             (cash REAL DEFAULT 200000, receivable REAL DEFAULT 0.0, inventory REAL DEFAULT 0.0, total_current_assets REAL DEFAULT 200000, buildings REAL DEFAULT 0.0, equipment REAL DEFAULT 0.0, fixtures REAL DEFAULT 0.0, total_fixed_assets REAL DEFAULT 0.0, total_assets REAL DEFAULT 200000, 
                              a_payable REAL DEFAULT 0.0, n_payable REAL DEFAULT 0.0, accruals REAL DEFAULT 0.0, total_current_liabilities REAL DEFAULT 0.0, mortgage REAL DEFAULT 0.0, long_term REAL DEFAULT 0.0, total_liabilities REAL DEFAULT 0.0, net_worth REAL DEFAULT 200000)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS income_statement
                             (sales REAL DEFAULT 1000000, cogs REAL DEFAULT 0.0, gross_profit REAL DEFAULT 1000000, payroll REAL 
                            DEFAULT 0.0, payroll_withold REAL DEFAULT 0.0, bills REAL DEFAULT 0.0, annual_expense REAL DEFAULT 0.0, total_expense REAL DEFAULT 0.0, other_income REAL DEFAULT 0.0, 
                              operating_income REAL DEFAULT 1000000, income_tax REAL DEFAULT 0.0, net_income REAL DEFAULT 1000000)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS payroll_history 
                            (date TEXT PRIMARY KEY, employee TEXT, dispursement REAL, witholding REAL, 
                            total_dispursement REAL DEFAULT 0.0, total_witholding REAL DEFAULT 0.0, salary REAL, 
                            bounce INTEGER DEFAULT 0, ftw REAL, stw REAL, ssn REAL, med REAL, paid REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS inventory 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, part TEXT, price REAL, quantity INTEGER, value REAL, reorder TEXT,
                            total REAL DEFAULT 0.0, cogpunit REAL DEFAULT 0.77, total_current REAL DEFAULT 0.0,
                            complete_unit INTEGER DEFAULT 1000, total_value REAL DEFAULT 770)''')

        self.cursor.execute('''
                            CREATE TRIGGER IF NOT EXISTS update_balance_sheet
                            AFTER UPDATE OF cash, receivable, inventory, buildings, equipment, fixtures, a_payable, n_payable, accruals, mortgage ON balance_sheet
                            BEGIN
                                UPDATE balance_sheet
                                SET total_current_assets = cash + receivable + inventory,
                                    total_fixed_assets = buildings + equipment + fixtures,
                                    total_assets = total_current_assets + total_fixed_assets,
                                    total_current_liabilities = a_payable + n_payable + accruals,
                                    long_term = mortgage,
                                    total_liabilities = total_current_liabilities + long_term,
                                    net_worth = total_assets - total_liabilities;
                            END;
                            ''')
        self.cursor.execute('''
                            CREATE TRIGGER IF NOT EXISTS update_balance_sheet2
                            AFTER UPDATE OF total_current_assets, total_fixed_assets, total_current_liabilities, long_term ON balance_sheet
                            BEGIN
                                UPDATE balance_sheet
                                SET total_assets = total_current_assets + total_fixed_assets,
                                    total_liabilities = total_current_liabilities + long_term,
                                    net_worth = total_assets - total_liabilities;
                            END;
                            ''')
        self.cursor.execute('''
                            CREATE TRIGGER IF NOT EXISTS update_balance_sheet3
                            AFTER UPDATE OF total_assets, total_liabilities ON balance_sheet
                            BEGIN
                                UPDATE balance_sheet
                                SET net_worth = total_assets - total_liabilities;
                            END;
                            ''')
        self.cursor.execute('''
                            CREATE TRIGGER IF NOT EXISTS update_income_statement
                            AFTER UPDATE OF sales, cogs, annual_expense, payroll, payroll_withold, bills ON income_statement
                            BEGIN
                                UPDATE income_statement
                                SET gross_profit = sales - cogs,
                                    total_expense = annual_expense + payroll + payroll_withold + bills;
                            END;
                            ''')
        self.cursor.execute('''
                            CREATE TRIGGER IF NOT EXISTS update_income_statement2
                            AFTER UPDATE OF gross_profit, total_expense ON income_statement
                            BEGIN
                                UPDATE income_statement
                                SET operating_income = gross_profit - total_expense;
                            END;
                            ''')
        self.cursor.execute('''
                            CREATE TRIGGER IF NOT EXISTS update_income_statement3
                            AFTER UPDATE OF other_income, operating_income, income_tax ON income_statement
                            BEGIN
                                UPDATE income_statement
                                SET net_income = other_income + operating_income - income_tax;
                            END;
                            ''')
        self.cursor.execute('''
                            CREATE TRIGGER IF NOT EXISTS employee_total_payroll
                            AFTER INSERT ON payroll_history
                            BEGIN
                                UPDATE payroll_history
                                SET total_dispursement = COALESCE((SELECT total_dispursement FROM payroll_history ORDER BY date DESC LIMIT 1 OFFSET 1), 0.0) + NEW.dispursement,
                                    total_witholding = COALESCE((SELECT total_witholding FROM payroll_history ORDER BY date DESC LIMIT 1 OFFSET 1), 0.0) + NEW.witholding
                                WHERE date = NEW.date;
                            END;
                            ''')
        self.cursor.execute('''
                            CREATE TRIGGER IF NOT EXISTS inventory_total
                            AFTER UPDATE OF quantity ON inventory
                            BEGIN
                                UPDATE inventory
                                SET value = quantity * price;
                            END;
                            ''')
        self.cursor.execute('''
                            CREATE TRIGGER IF NOT EXISTS inventory_total2
                            AFTER INSERT ON inventory
                            BEGIN
                                UPDATE inventory
                                SET total = COALESCE((SELECT total FROM inventory ORDER BY id DESC LIMIT 1 OFFSET 1), 0.0) + NEW.value
                                WHERE id = NEW.id;
                            END;
                            ''')


        self.connection.commit()

        self.cursor.execute("SELECT COUNT(*) FROM balance_sheet")
        bs_count = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM income_statement")
        is_count = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM inventory")
        i_count = self.cursor.fetchone()[0]

        if bs_count < 1:
            self.cursor.execute("INSERT INTO balance_sheet DEFAULT VALUES")
        if is_count < 1:
            self.cursor.execute("INSERT INTO income_statement DEFAULT VALUES")
        if i_count < 1:
            self.cursor.execute("INSERT INTO inventory DEFAULT VALUES")
            self.connection.commit()

        self.master.geometry("850x900")

        # Header with green background
        header_text = "ENG566 Computer Program"
        self.header_label = tk.Label(self.master, text=header_text, bg="green", fg="white", font=("Arial", 25, "bold"), pady=10)
        self.header_label.pack(fill="x")  # Fill the header label horizontally

        self.list_employees_button = tk.Button(self.master, text="List Employees", command=self.list_employees, height=2, width=350, bd=0, font=("Arial", 14))
        self.list_employees_button.pack(pady=(20, 0))

        self.add_employee_button = tk.Button(self.master, text="Add Employee", command=self.add_employee, height=2, width=350, bd=0, font=("Arial", 14))
        self.add_employee_button.pack()

        self.list_vendor_button = tk.Button(self.master, text="List Vendors", command=self.list_vendors, height=2, width=350, bd=0, font=("Arial", 14))
        self.list_vendor_button.pack(pady=(20, 0))

        self.add_vendor_button = tk.Button(self.master, text="Add Vendor", command=self.add_vendor, height=2, width=350, bd=0, font=("Arial", 14))
        self.add_vendor_button.pack(pady=0)

        self.list_customers_button = tk.Button(self.master, text="List Customers", command=self.list_customers, height=2, width=350, bd=0, font=("Arial", 14))
        self.list_customers_button.pack(pady=(20, 0))

        self.add_customers_button = tk.Button(self.master, text="Add Customers", command=self.add_customer, height=2, width=350, bd=0, font=("Arial", 14))
        self.add_customers_button.pack(pady=0)

        self.pay_employee_button = tk.Button(self.master, text="Pay Employee", command=self.pay_employee, height=2, width=350, bd=0, font=("Arial", 14))
        self.pay_employee_button.pack(pady=(20, 0))

        self.payroll_button = tk.Button(self.master, text="Payroll", command=self.list_payroll, height=2, width=350, bd=0, font=("Arial", 14))
        self.payroll_button.pack(pady=0)

        self.inventory_button = tk.Button(self.master, text="Inventory", command=self.list_inventory, height=2, width=350, bd=0, font=("Arial", 14))
        self.inventory_button.pack(pady=20)

        self.create_invoice_button = tk.Button(self.master, text="Create Invoice", command=self.create_invoice, height=2, width=350, bd=0, font=("Arial", 14))
        self.create_invoice_button.pack()

        self.invoice_history_button = tk.Button(self.master, text="Invoice History", command=self.edit_employee, height=2, width=350, bd=0, font=("Arial", 14))
        self.invoice_history_button.pack(pady=0)

        self.create_PO_button = tk.Button(self.master, text="Create PO", command=self.create_PO, height=2, width=350, bd=0, font=("Arial", 14))
        self.create_PO_button.pack(pady=(20, 0))

        self.PO_history_button = tk.Button(self.master, text="PO History", command=self.edit_employee, height=2, width=350, bd=0, font=("Arial", 14))
        self.PO_history_button.pack(pady=0)

        self.balance_sheet_button = tk.Button(self.master, text="Balance Sheet", command=self.show_balance_sheet, height=2, width=350, bd=0, font=("Arial", 14))
        self.balance_sheet_button.pack(pady=(20, 0))

        self.income_statement_button = tk.Button(self.master, text="Income Statement", command=self.show_income_statement, height=2, width=350, bd=0, font=("Arial", 14))
        self.income_statement_button.pack(pady=0)
        
    def list_employees(self):
        print("Listing employees...")
        ListEmployeeForm(self, self.cursor)
        
    def add_employee(self):
        print("Adding employee...")
        AddEmployeeForm(self)

    def add_employee_to_database(self, first_name, last_name, address1, address2, city, state, zip_code, ssn, withold, salary):
        print("Employee Added")
        self.cursor.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (first_name, last_name, address1, address2, city, state, zip_code, ssn, withold, salary))
        self.connection.commit()

    def list_customers(self):
        print("Listing Customers...")
        ListCustomersForm(self, self.cursor)

    def add_customer(self):
        print("Adding Customer...")
        AddCustomerForm(self)

    def add_customer_to_database(self, company, last_name, first_name, address1, city, state, zip_code, price):
        print("Customer Added")
        self.cursor.execute("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (company, last_name, first_name, address1, city, state, zip_code, price))
        self.connection.commit()

    def list_vendors(self):
        print("Listing Vendors...")
        ListVendorsForm(self, self.cursor)

    def add_vendor(self):
        print("Adding Vendor...")
        AddVendorForm(self)

    def add_vendor_to_database(self, company, part, price, address1, address2, city, state, zip_code):
        self.cursor.execute("INSERT INTO vendors VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (company, part, price, address1, address2, city, state, zip_code))
        self.connection.commit()

    def pay_employee(self):
        print("Paying Employee")
        PayEmployee(self, self.cursor)

    def add_payroll(self, employee, payroll):
        print("Adding Payroll")
        self.cursor.execute("UPDATE balance_sheet SET cash = cash - ?", (payroll,))
        self.cursor.execute("UPDATE income_statement SET payroll = payroll + ?, payroll_withold = payroll_withold + ?", (payroll*(1-self.payroll_withold), payroll*self.payroll_withold))
        query = f"INSERT INTO payroll_history (date, employee, dispursement, witholding, salary, ftw, stw, ssn, med, paid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, (datetime.now(), employee, payroll*(1-self.payroll_withold), payroll*self.payroll_withold, payroll, payroll*self.federal_tax_withold, payroll*self.state_tax_withold, payroll*self.ssn_withold, payroll*self.medicare_withold, payroll*(1-self.payroll_withold)))
        self.connection.commit()

    def list_payroll(self):
        print("Listing Payroll History")
        ListPayroll(self, self.cursor)

    def list_inventory(self):
        print("Listing Inventory")
        ListInventory(self, self.cursor)

    def create_invoice(self):
        print("Creating Invoice")
        CreateInvoice(self, self.cursor)
    
    def show_balance_sheet(self):
        print("Showing Balance Sheet")
        ShowBalanceSheet(self, self.cursor)

    def show_income_statement(self):
        print("Showing Income Statement")
        ShowIncomeStatement(self, self.cursor)

    def add_invoice_history(self, customer, units):
        print("Adding invoice to history")
        self.cursor.execute("SELECT price FROM customers WHERE company_name = ?", (customer,))
        price = self.cursor.fetchone()[0]
        total_receivable = price * units
        self.cursor.execute("UPDATE balance_sheet SET receivable = receivable + ?", (total_receivable,))

        self.cursor.execute("SELECT cogpunit FROM inventory ORDER BY id DESC LIMIT 1")
        cogpunit = self.cursor.fetchone()[0]
        cog = cogpunit * units
        self.cursor.execute("UPDATE income_statement SET sales = sales + ?, cogs = cogs + ?", (total_receivable, cog))
        self.cursor.execute("UPDATE inventory SET complete_unit = complete_unit - ?, total_value = total_value - ?", (units, cog))

        self.connection.commit()

    def create_PO(self):
        print("Creating PO")
        CreatePO(self, self.cursor)

    def add_PO_history(self, part, quantity):
        print("Adding PO to history")
        self.cursor.execute("SELECT price FROM vendors WHERE part = ?", (part,))
        price = self.cursor.fetchone()[0]
        total_buy = price * quantity
        self.cursor.execute("UPDATE balance_sheet SET inventory = inventory + ?, a_payable = a_payable + ?", (total_buy, total_buy))

        self.cursor.execute("UPDATE income_statement SET cogs = cogs + ?", (total_buy,))

        self.cursor.execute("SELECT COUNT(*) FROM inventory WHERE part = ?", (part,))


        result = self.cursor.fetchone()[0]
        if result == 0:
            self.cursor.execute("INSERT INTO inventory (part, price, quantity, value) VALUES (?, ?, ?, ?)", (part, price, quantity, price*quantity))
        else:
            self.cursor.execute("UPDATE inventory SET quantity = quantity + ? WHERE part = ?", (quantity, part))

        self.connection.commit()

    def remove_employee(self):
        None

    def edit_employee(self):
        None        

root = tk.Tk()
app = EmployeeAppMenu(root)
root.mainloop()