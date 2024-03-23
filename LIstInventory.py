import tkinter as tk
from tkinter import ttk

class ListInventory:
    def __init__(self, master, cursor):
        self.master = master
        self.cursor = cursor
        self.window = tk.Toplevel()
        self.window.title("List Inventory")
        self.window.geometry("1200x900")

        # Header with green background
        self.topFrame = tk.Frame(self.window)
        self.topFrame.grid(row=0, columnspan=4, sticky="ew")

        header_text = "Inventory"
        self.header_label = tk.Label(self.topFrame, text=header_text, bg="green", fg="white", font=("Arial", 18, "bold"), pady=5, width=75, anchor="w")
        self.header_label.grid(row=0, columnspan=10, pady=10, sticky="w")

        label1 = ["Part",
                  "Price/Unit",
                  "Quantity",
                  "Value",
                  "Re-order"]
        
        for i, label in enumerate(label1):
            tk.Label(self.topFrame, text=label, font=("Arial", 14, "bold"), bg="light green", fg="black").grid(row=1, column=i, sticky="w", padx=(0, 10), pady=(10, 5))

        cursor.execute("SELECT part, price, quantity, value, reorder FROM inventory ORDER BY id DESC")
        histories = cursor.fetchall()

        for i, history in enumerate(histories):
            for j, col in enumerate(history):
                if j==1 and col==None:
                    break
                if j==1 or j==3:
                    tk.Label(self.topFrame, text=f"${col}").grid(row=i+2, column=j, sticky="w", padx=(0, 10), pady=5)
                else:
                    tk.Label(self.topFrame, text=col).grid(row=i+2, column=j, sticky="w", padx=(0, 10), pady=5)

        self.midFrame = tk.Frame(self.window)
        self.midFrame.grid(columnspan=2, sticky="ew")

        label2 = ["Total",
                  "COG/Unit",
                  "Total Units that can be built from current parts"]
        
        for i, label in enumerate(label2):
            tk.Label(self.midFrame, text=label, font=("Arial", 14, "bold"), bg="light green", fg="black").grid(row=0, column=i, sticky="w", padx=(0, 10), pady=(10, 5))
        
        cursor.execute("SELECT total, cogpunit, total_current FROM inventory ORDER BY id DESC LIMIT 1")
        totals = cursor.fetchone()

        if totals:
            for i, col in enumerate(totals):
                tk.Label(self.midFrame, text=f"${col}").grid(row=1, column=i, sticky="w", padx=(0, 10), pady=5)

        self.botFrame = tk.Frame(self.window)
        self.botFrame.grid(columnspan=2, sticky="ew")

        label3 = ["Complete Units in Stock",
                  "Total Value"]
        
        for i, label in enumerate(label3):
            tk.Label(self.botFrame, text=label, font=("Arial", 14, "bold"), bg="light green", fg="black").grid(row=0, column=i, sticky="w", padx=(0, 10), pady=(10, 5))
        
        cursor.execute("SELECT complete_unit, total_value FROM inventory ORDER BY id DESC LIMIT 1")
        payments = cursor.fetchone()
        
        if payments:
            for i, col in enumerate(payments):
                if i ==1:
                    tk.Label(self.botFrame, text=f"${col}").grid(row=1, column=i, sticky="w", padx=(0, 10), pady=5)
                else:
                    tk.Label(self.botFrame, text=col).grid(row=1, column=i, sticky="w", padx=(0, 10), pady=5)