import tkinter as tk
from tkinter import ttk

class ListPayroll:
    def __init__(self, master, cursor):
        self.master = master
        self.cursor = cursor
        self.window = tk.Toplevel()
        self.window.title("List Payroll")
        self.window.geometry("1200x900")

        # Header with green background
        self.topFrame = tk.Frame(self.window)
        self.topFrame.grid(row=0, columnspan=4, sticky="ew")

        header_text = "Payroll Payments/History"
        self.header_label = tk.Label(self.topFrame, text=header_text, bg="green", fg="white", font=("Arial", 18, "bold"), pady=5, width=75, anchor="w")
        self.header_label.grid(row=0, columnspan=10, pady=10, sticky="w")

        label1 = ["Data Paid",
                  "Employee",
                  "Dispursement",
                  "Witholding"]
        
        for i, label in enumerate(label1):
            tk.Label(self.topFrame, text=label, font=("Arial", 14, "bold"), bg="light green", fg="black").grid(row=1, column=i, sticky="w", padx=(0, 10), pady=(10, 5))

        cursor.execute("SELECT date, employee, dispursement, witholding FROM payroll_history ORDER BY date DESC")
        histories = cursor.fetchall()

        for i, history in enumerate(histories):
            for j, col in enumerate(history):
                if j>= 2:
                    tk.Label(self.topFrame, text=f"${col}").grid(row=i+2, column=j, sticky="w", padx=(0, 10), pady=5)
                else:
                    tk.Label(self.topFrame, text=col).grid(row=i+2, column=j, sticky="w", padx=(0, 10), pady=5)

        self.midFrame = tk.Frame(self.window)
        self.midFrame.grid(columnspan=2, sticky="ew")

        label2 = ["Total Dispursement",
                  "Total Witholding"]
        
        for i, label in enumerate(label2):
            tk.Label(self.midFrame, text=label, font=("Arial", 14, "bold"), bg="light green", fg="black").grid(row=0, column=i, sticky="w", padx=(0, 10), pady=(10, 5))
        
        cursor.execute("SELECT total_dispursement, total_witholding FROM payroll_history ORDER BY date DESC LIMIT 1")
        totals = cursor.fetchone()

        if totals:
            for i, col in enumerate(totals):
                tk.Label(self.midFrame, text=f"${col}").grid(row=1, column=i, sticky="w", padx=(0, 10), pady=5)

        self.botFrame = tk.Frame(self.window)
        self.botFrame.grid(columnspan=2, sticky="ew")

        label3 = ["Salary",
                  "Bounce",
                  "Federal Tax Witheld",
                  "State Tax Witheld",
                  "Social Security",
                  "Medicare",
                  "Amount Paid"]
        
        for i, label in enumerate(label3):
            tk.Label(self.botFrame, text=label, font=("Arial", 14, "bold"), bg="light green", fg="black").grid(row=0, column=i, sticky="w", padx=(0, 10), pady=(10, 5))
        
        cursor.execute("SELECT salary, bounce, ftw, stw, ssn, med, paid FROM payroll_history")
        payments = cursor.fetchall()
        
        for i, payment in enumerate(payments):
            for j, col in enumerate(payment):
                    tk.Label(self.botFrame, text=col).grid(row=i+1, column=j, sticky="w", padx=(0, 10), pady=5)