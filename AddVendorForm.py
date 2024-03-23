import tkinter as tk

class AddVendorForm:
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel()
        self.window.title("Add Vendor")
        self.window.geometry("800x900")

        # Header with green background
        header_text = "Add Vendor"
        self.header_label = tk.Label(self.window, text=header_text, bg="green", fg="white", font=("Arial", 18, "bold"), pady=5, width=73)
        self.header_label.grid(row=0, columnspan=10, pady=10)
        
        self.company_name_label = tk.Label(self.window, text="Company Name:", anchor="w", fg="green")
        self.company_name_label.grid(row=1, padx=5, pady=(10, 0), sticky="w")
        self.company_name_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.company_name_entry.grid(row=2, padx=5)

        self.part_label = tk.Label(self.window, text="Part", anchor="w", fg="green")
        self.part_label.grid(row=3, padx=5, pady=(10, 0), sticky="w")
        self.part_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.part_entry.grid(row=4, padx=5)

        self.price_label = tk.Label(self.window, text="Price/Unit (Dollars):", anchor="w", fg="green")
        self.price_label.grid(row=5, padx=5, pady=(10, 0), sticky="w")
        self.price_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.price_entry.grid(row=6, padx=5)

        self.address1_label = tk.Label(self.window, text="Address 1:", anchor="w", fg="green")
        self.address1_label.grid(row=7, padx=5, pady=(10, 0), sticky="w")
        self.address1_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.address1_entry.grid(row=8, padx=5)

        self.address2_label = tk.Label(self.window, text="Address 2:", anchor="w", fg="green")
        self.address2_label.grid(row=9, padx=5, pady=(10, 0), sticky="w")
        self.address2_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.address2_entry.grid(row=10, padx=5)

        self.city_label = tk.Label(self.window, text="City:", anchor="w", fg="green")
        self.city_label.grid(row=11, padx=5, pady=(10, 0), sticky="w")
        self.city_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.city_entry.grid(row=12, padx=5)

        self.state_label = tk.Label(self.window, text="State:", anchor="w", fg="green")
        self.state_label.grid(row=13, padx=5, pady=(10, 0), sticky="w")
        self.state_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.state_entry.grid(row=14, padx=5)

        self.zip_label = tk.Label(self.window, text="Zip Code:", anchor="w", fg="green")
        self.zip_label.grid(row=15, padx=5, pady=(10, 0), sticky="w")
        self.zip_entry = tk.Entry(self.window, width=65, font=("Arial", 20))
        self.zip_entry.grid(row=16, padx=5)

        self.add_button = tk.Button(self.window, text="Add Vendor", command=self.add_vendor, height=2, width=65)
        self.add_button.grid(row=17, pady=30)

    def add_vendor(self):
        company_name = self.company_name_entry.get()
        part = self.part_entry.get()
        price = self.price_entry.get()
        address1 = self.address1_entry.get()
        address2 = self.address2_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        zip = self.zip_entry.get()
        zip = int(zip)
        price = float(price)

        self.master.add_vendor_to_database(company_name, part, price, address1, address2, city, state, zip)
        self.window.destroy()