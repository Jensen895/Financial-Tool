import tkinter as tk
from tkinter import ttk

class CreateInvoice:
    def __init__(self, master, cursor):
        self.master = master
        self.cursor = cursor
        self.window = tk.Toplevel()
        self.window.title("Create Invoice")
        self.window.geometry("1200x900")

        # Header with green background
        self.topFrame = tk.Frame(self.window)
        self.topFrame.grid(row=0, columnspan=2, sticky="ew")

        header_text = "Create Invoice"
        self.header_label = tk.Label(self.topFrame, text=header_text, bg="green", fg="white", font=("Arial", 18, "bold"), pady=5, width=75, anchor="w")
        self.header_label.grid(row=0, columnspan=10, pady=10, sticky="w")

        cursor.execute("SELECT company_name FROM customers")
        names = cursor.fetchall()

        self.botFrame = tk.Frame(self.window)
        self.botFrame.grid(row=1, columnspan=2, sticky="ew")
        
        tk.Label(self.topFrame, text="Customer: ").grid(row=1, column=0, padx=(5, 0), pady=5, sticky="w")
        self.combobox = ttk.Combobox(self.topFrame, values=names, width=10)
        self.combobox.grid(row=1, column=1, pady=2, sticky="w")

        tk.Label(self.botFrame, text="Number of Units to Invoice:").grid(row=0, padx=(5, 0), pady=5, sticky="w")
        self.entry = tk.Entry(self.botFrame, width=65, font=("Arial", 20))
        self.entry.grid(row=1, padx=5)

        cursor.execute("SELECT complete_unit FROM inventory ORDER BY id DESC LIMIT 1")
        complete_unit = cursor.fetchone()[0]
        tk.Label(self.botFrame, text=f"Number of Units in Stock: {complete_unit}").grid(row=2, padx=(10, 5), pady=5, sticky="w")
        tk.Button(self.botFrame, width=20, height=2, text="Create Invoice", command=self.add_invoice).grid(row=3, pady=10, padx=5)

    def add_invoice(self):
        customer = self.combobox.get()
        units = self.entry.get()
        units = int(units)
        self.master.add_invoice_history(customer, units)
        self.window.destroy()