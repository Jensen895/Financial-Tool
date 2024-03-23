import tkinter as tk
from tkinter import ttk

class CreatePO:
    def __init__(self, master, cursor):
        self.master = master
        self.cursor = cursor
        self.window = tk.Toplevel()
        self.window.title("Create PO")
        self.window.geometry("1200x900")

        # Header with green background
        self.topFrame = tk.Frame(self.window)
        self.topFrame.grid(row=0, columnspan=2, sticky="ew")

        header_text = "Create PO"
        self.header_label = tk.Label(self.topFrame, text=header_text, bg="green", fg="white", font=("Arial", 18, "bold"), pady=5, width=75, anchor="w")
        self.header_label.grid(row=0, columnspan=10, pady=10, sticky="w")

        cursor.execute("SELECT part FROM vendors")
        names = cursor.fetchall()

        self.botFrame = tk.Frame(self.window)
        self.botFrame.grid(row=1, columnspan=2, sticky="ew")
        
        tk.Label(self.topFrame, text="Part: ").grid(row=1, column=0, padx=(5, 0), pady=5, sticky="w")
        self.combobox = ttk.Combobox(self.topFrame, values=names, width=10)
        self.combobox.grid(row=1, column=1, pady=2, sticky="w")

        tk.Label(self.botFrame, text="Quantity:").grid(row=0, padx=(5, 0), pady=5, sticky="w")
        self.entry = tk.Entry(self.botFrame, width=65, font=("Arial", 20))
        self.entry.grid(row=1, padx=5)

        tk.Button(self.botFrame, width=20, height=2, text="Create PO", command=self.add_PO).grid(row=2, pady=10, padx=5)

    def add_PO(self):
        part = self.combobox.get()
        quantity = self.entry.get()
        quantity = int(quantity)
        self.master.add_PO_history(part, quantity)
        self.window.destroy()