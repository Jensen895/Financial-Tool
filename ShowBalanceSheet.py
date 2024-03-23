import tkinter as tk

class ShowBalanceSheet:
    def __init__(self, master, cursor):
        # Initialize the Tkinter window
        window = tk.Toplevel()
        window.title("Balance Sheet")
        window.geometry("1200x900")

        # Header with green background
        header_text = "Balance Sheet"
        self.header_label = tk.Label(window, text=header_text, bg="green", fg="white", font=("Arial", 18, "bold"), pady=5, width=75, anchor="w")
        self.header_label.grid(row=0, columnspan=10, pady=10, sticky="w")

        # Balance sheet data as a list of strings
        balance_sheet_data = [
            "Cash",
            "Accounts Receivable",
            "Inventory",
            "Total Current Assets",
            "Land/Buildings",
            "Equipment",
            "Furniture and Fixtures",
            "Total Fixed Assets",
            "Total Assets",
            "Accounts Payable",
            "Notes Payable",
            "Accruals",
            "Total Current Liabilities",
            "Mortgage",
            "Total Long Term Debt",
            "Total Liabilities",
            "Net Worth",
        ]

        # Create labels and entries for the balance sheet data
        cursor.execute("SELECT * FROM balance_sheet LIMIT 1")
        entries = cursor.fetchone()

        if entries is not None:
            for i, val in enumerate(entries):
                row = i % 9 + 1
                column = (i // 9) * 2

                if i >= 15:
                    tk.Label(window, text=balance_sheet_data[i]).grid(row=row+1, column=column, padx=(5, 180), pady=5, sticky="w")
                    tk.Label(window, text=f"${val}").grid(row=row+1, column=column+1, padx=5, pady=5, sticky="e")
                else:
                    tk.Label(window, text=balance_sheet_data[i]).grid(row=row, column=column, padx=(5, 180), pady=5, sticky="w")
                    tk.Label(window, text=f"${val}").grid(row=row, column=column+1, padx=5, pady=5, sticky="e")
