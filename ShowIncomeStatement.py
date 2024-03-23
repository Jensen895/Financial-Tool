import tkinter as tk

class ShowIncomeStatement:
    def __init__(self, master, cursor):
        # Initialize the Tkinter window
        window = tk.Toplevel()
        window.title("Income Statement")
        window.geometry("1200x900")

        # Header with green background
        header_text = "Income Statement"
        self.header_label = tk.Label(window, text=header_text, bg="green", fg="white", font=("Arial", 18, "bold"), pady=5, width=75, anchor="w")
        self.header_label.grid(row=0, columnspan=10, pady=10, sticky="w")

        # Balance sheet data as a list of strings
        income_statement_data = [
            "Sales",
            "COGS",
            "Gross Profit",
            "Payroll",
            "Payroll Witholding",
            "Bills",
            "Annual Expenses",
            "Total Expenses",
            "Other Income",
            "Operating Income",
            "Income Taxes",
            "Net Income"
        ]

        # Create labels and entries for the balance sheet data
        cursor.execute("SELECT * FROM income_statement LIMIT 1")
        entries = cursor.fetchone()

        if entries is not None:
            for i, val in enumerate(entries):
                if i == 0:
                    tk.Label(window, text="Sales", font=("Arial", 18, "bold")).grid(row=1, padx=(5, 180), pady=(15, 5), sticky="w")
                elif i == 3:
                    tk.Label(window, text="Expenses", font=("Arial", 18, "bold")).grid(row=5, padx=(5, 180), pady=(15, 5), sticky="w")
                elif i == 8:
                    tk.Label(window, text="", font=("Arial", 18, "bold")).grid(row=11, padx=(5, 180), pady=5, sticky="w")

                if  0 <= i < 3:
                    tk.Label(window, text=income_statement_data[i]).grid(row=i+2, column=0, padx=(5, 180), pady=5, sticky="w")
                    tk.Label(window, text=f"${val}").grid(row=i+2, column=1, padx=5, pady=5, sticky="e")
                elif  3 <= i < 8:
                    tk.Label(window, text=income_statement_data[i]).grid(row=i+3, column=0, padx=(5, 180), pady=5, sticky="w")
                    tk.Label(window, text=f"${val}").grid(row=i+3, column=1, padx=5, pady=5, sticky="e")
                else:
                    tk.Label(window, text=income_statement_data[i]).grid(row=i+4, column=0, padx=(5, 180), pady=5, sticky="w")
                    tk.Label(window, text=f"${val}").grid(row=i+4, column=1, padx=5, pady=5, sticky="e")
                

