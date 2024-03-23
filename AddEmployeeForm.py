import tkinter as tk

class AddEmployeeForm:
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel()
        self.window.title("Add Employee")
        self.window.geometry("800x900")

        # Header with green background
        header_text = "Add Employee"
        self.header_label = tk.Label(self.window, text=header_text, bg="green", fg="white", font=("Arial", 18, "bold"), pady=5, width=73)
        self.header_label.grid(row=0, columnspan=10, pady=10)
        
        self.first_name_label = tk.Label(self.window, text="First Name:", anchor="w", fg="green")
        self.first_name_label.grid(row=1, padx=5, pady=(10, 0), sticky="w")
        self.first_name_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.first_name_entry.grid(row=2, padx=5)

        self.last_name_label = tk.Label(self.window, text="Last Name:", anchor="w", fg="green")
        self.last_name_label.grid(row=3, padx=5, pady=(10, 0), sticky="w")
        self.last_name_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.last_name_entry.grid(row=4, padx=5)

        self.address1_label = tk.Label(self.window, text="Address 1:", anchor="w", fg="green")
        self.address1_label.grid(row=5, padx=5, pady=(10, 0), sticky="w")
        self.address1_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.address1_entry.grid(row=6, padx=5)

        self.address2_label = tk.Label(self.window, text="Address 2:", anchor="w", fg="green")
        self.address2_label.grid(row=7, padx=5, pady=(10, 0), sticky="w")
        self.address2_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.address2_entry.grid(row=8, padx=5)

        self.city_label = tk.Label(self.window, text="City:", anchor="w", fg="green")
        self.city_label.grid(row=9, padx=5, pady=(10, 0), sticky="w")
        self.city_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.city_entry.grid(row=10, padx=5)

        self.state_label = tk.Label(self.window, text="State:", anchor="w", fg="green")
        self.state_label.grid(row=11, padx=5, pady=(10, 0), sticky="w")
        self.state_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.state_entry.grid(row=12, padx=5)

        self.zip_label = tk.Label(self.window, text="Zip Code:", anchor="w", fg="green")
        self.zip_label.grid(row=13, padx=5, pady=(10, 0), sticky="w")
        self.zip_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.zip_entry.grid(row=14, padx=5)

        self.ssn_label = tk.Label(self.window, text="Social Security Number (numbers only):", anchor="w", fg="green")
        self.ssn_label.grid(row=15, padx=5, pady=(10, 0), sticky="w")
        self.ssn_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.ssn_entry.grid(row=16, padx=5)

        self.withold_label = tk.Label(self.window, text="Witholdings:", anchor="w", fg="green")
        self.withold_label.grid(row=17, padx=5, pady=(10, 0), sticky="w")
        self.withold_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.withold_entry.grid(row=18, padx=5)

        self.salary_label = tk.Label(self.window, text="Salary (Dollars):", anchor="w", fg="green")
        self.salary_label.grid(row=19, padx=5, pady=(10, 0), sticky="w")
        self.salary_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.salary_entry.grid(row=20, padx=5)

        self.add_button = tk.Button(self.window, text="Add Employee", command=self.add_employee, height=2, width=65)
        self.add_button.grid(row=21, pady=30)

    def add_employee(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        address1 = self.address1_entry.get()
        address2 = self.address2_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        zip = self.zip_entry.get()
        zip = int(zip)
        ssn = self.ssn_entry.get()
        ssn = int(ssn)
        withold = self.withold_entry.get()
        withold = int(withold)
        salary = self.salary_entry.get()
        salary = int(salary)

        self.master.add_employee_to_database(first_name, last_name, address1, address2, city, state, zip, ssn, withold, salary)
        self.window.destroy()