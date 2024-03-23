import tkinter as tk
from tkinter import ttk

class PayEmployee:
    def __init__(self, master, cursor):
        self.master = master
        self.cursor = cursor
        self.window = tk.Toplevel()
        self.window.title("Pay Employee")
        self.window.geometry("1200x900")

        # Header with green background
        self.topFrame = tk.Frame(self.window)
        self.topFrame.grid(row=0, columnspan=2, sticky="ew")

        header_text = "Pay Employee"
        self.header_label = tk.Label(self.topFrame, text=header_text, bg="green", fg="white", font=("Arial", 18, "bold"), pady=5, width=75, anchor="w")
        self.header_label.grid(row=0, columnspan=10, pady=10, sticky="w")

        cursor.execute("SELECT last_name FROM employees")
        names = cursor.fetchall()

        self.botFrame = tk.Frame(self.window)
        self.botFrame.grid(row=1, columnspan=2, sticky="ew")
        
        tk.Label(self.topFrame, text="Employee: ").grid(row=1, column=0, padx=(5, 0), pady=5, sticky="w")
        self.combobox = ttk.Combobox(self.topFrame, values=names, width=10)
        self.combobox.grid(row=1, column=1, pady=2, sticky="w")

        tk.Button(self.botFrame, width=20, height=2, text="Pay Employee", command=self.add_payroll).grid(row=2, pady=10, padx=5)

    def add_payroll(self):
        employee = self.combobox.get()
        self.cursor.execute("SELECT salary FROM employees WHERE last_name = ?", (employee,))
        payroll = self.cursor.fetchone()[0]
        payroll = float(payroll)

        self.master.add_payroll(employee, payroll)
        self.window.destroy()