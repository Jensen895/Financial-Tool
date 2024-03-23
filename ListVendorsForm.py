import tkinter as tk

class ListVendorsForm:
    def __init__(self, master, cursor):
        window = tk.Toplevel()
        window.title("List Vendors")
        window.geometry("1200x900")

        # Header with green background
        header_text = "Vendor Data"
        self.header_label = tk.Label(window, text=header_text, bg="green", fg="white", font=("Arial", 18, "bold"), pady=5, width=75, anchor="w")
        self.header_label.grid(row=0, columnspan=10, pady=10, sticky="w")
        
        # Fetch data from the database
        cursor.execute("SELECT * FROM vendors")
        vendors = cursor.fetchall()

        # Header row
        self.header_frame = tk.Frame(window, bg="light green", height=25)
        self.header_frame.grid(row=1, column=0, columnspan=10, sticky="ew")
        header_labels = ["Company Name", "Part", "Price/Unit", "Address 1", "Address 2","City", "State", "Zip"]
        for col, label in enumerate(header_labels):
            tk.Label(window, text=label, font=("Arial", 14, "bold"), bg="light green", fg="black").grid(row=1, column=col, sticky="w", padx=(0, 10), pady=5)

        # Create labels to display employee data
        for i, vendor in enumerate(vendors, start=2):
            for col, value in enumerate(vendor):
                tk.Label(window, text=value).grid(row=i, column=col, sticky="w", padx=(2, 10), pady=2)
