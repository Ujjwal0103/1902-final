import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from data_handler import add_expense, add_income, save_data, get_all_income, get_all_expenses
from models import Expense, Income
from visualization import plot_expenses_by_category, plot_monthly_income_expenses

# Initialize main window
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("500x400")

# Helper functions
def add_expense_gui():
    try:
        amount = float(expense_amount_entry.get())
        category = expense_category_entry.get()
        date = datetime.strptime(expense_date_entry.get(), "%Y-%m-%d").date()
        description = expense_description_entry.get()
        expense = Expense(amount=amount, category=category, date=date, description=description)
        add_expense(expense)
        messagebox.showinfo("Success", "Expense added successfully!")
        update_summary()
    except Exception as e:
        messagebox.showerror("Error", f"Could not add expense: {e}")

def add_income_gui():
    try:
        amount = float(income_amount_entry.get())
        source = income_source_entry.get()
        date = datetime.strptime(income_date_entry.get(), "%Y-%m-%d").date()
        income = Income(amount=amount, source=source, date=date)
        add_income(income)
        messagebox.showinfo("Success", "Income added successfully!")
        update_summary()
    except Exception as e:
        messagebox.showerror("Error", f"Could not add income: {e}")

def view_expenses_by_category_gui():
    plot_expenses_by_category()

def view_monthly_income_expenses_gui():
    try:
        year = int(year_entry.get())
        month = int(month_entry.get())
        plot_monthly_income_expenses(year, month)
    except Exception as e:
        messagebox.showerror("Error", f"Could not plot data: {e}")

def reset_data_on_exit():
    initial_data = {"expenses": [], "income": []}
    save_data(initial_data)  # Save empty data to reset the file
    root.destroy()  # Close the window

# Bind the close window event to the reset function
root.protocol("WM_DELETE_WINDOW", reset_data_on_exit)

def view_expenses_gui():
    try:
        # Create a new window
        view_window = tk.Toplevel(root)
        view_window.title("View and Delete Expenses")
        view_window.geometry("400x300")

        # Create a frame to display expenses
        expenses_frame = tk.Frame(view_window)
        expenses_frame.pack(fill="both", expand=True)

        # Add a scrollbar
        scrollbar = tk.Scrollbar(expenses_frame)
        scrollbar.pack(side="right", fill="y")

        # Create a Listbox to display expenses
        expenses_listbox = tk.Listbox(expenses_frame, yscrollcommand=scrollbar.set, width=50, height=15)
        expenses_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=expenses_listbox.yview)

        # Load expenses
        from data_handler import get_all_expenses  # Import function to fetch all expenses
        expenses = get_all_expenses()
        for i, expense in enumerate(expenses):
            expenses_listbox.insert(tk.END, f"{i + 1}. {expense['description']} - ${expense['amount']} ({expense['category']}) on {expense['date']}")

        # Function to delete selected expense
        def delete_selected_expense():
            try:
                selected_index = expenses_listbox.curselection()
                if not selected_index:
                    raise Exception("No expense selected")
                selected_index = selected_index[0]  # Get the selected item's index
                del expenses[selected_index]  # Delete the selected expense from the list
                save_data({"expenses": expenses, "income": []})  # Save updated data
                expenses_listbox.delete(selected_index)  # Remove from the listbox
                messagebox.showinfo("Success", "Expense deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete expense: {e}")

        # Add a delete button
        delete_button = tk.Button(view_window, text="Delete Selected Expense", command=delete_selected_expense)
        delete_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Could not load expenses: {e}")


def view_income_gui():
    try:
        # Create a new window
        view_window = tk.Toplevel(root)
        view_window.title("View and Delete Income")
        view_window.geometry("400x300")

        # Create a frame to display income
        income_frame = tk.Frame(view_window)
        income_frame.pack(fill="both", expand=True)

        # Add a scrollbar
        scrollbar = tk.Scrollbar(income_frame)
        scrollbar.pack(side="right", fill="y")

        # Create a Listbox to display income
        income_listbox = tk.Listbox(income_frame, yscrollcommand=scrollbar.set, width=50, height=15)
        income_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=income_listbox.yview)

        # Load income
        from data_handler import get_all_income  # Import function to fetch all income
        income_data = get_all_income()
        for i, income in enumerate(income_data):
            income_listbox.insert(
                tk.END, f"{i + 1}. {income['source']} - ${income['amount']} on {income['date']}"
            )

        # Function to delete selected income
        def delete_selected_income():
            try:
                selected_index = income_listbox.curselection()
                if not selected_index:
                    raise Exception("No income selected")
                selected_index = selected_index[0]  # Get the selected item's index
                del income_data[selected_index]  # Delete the selected income from the list
                save_data({"expenses": [], "income": income_data})  # Save updated data
                income_listbox.delete(selected_index)  # Remove from the listbox
                messagebox.showinfo("Success", "Income deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete income: {e}")

        # Add a delete button
        delete_button = tk.Button(view_window, text="Delete Selected Income", command=delete_selected_income)
        delete_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Could not load income: {e}")

def update_summary():
    try:
        # Fetch all income and expenses
        income_data = get_all_income()
        expense_data = get_all_expenses()

        # Filter data for the current month
        selected_month = int(month_var.get())
        selected_year = int(year_var.get())

        total_income = sum(
            entry["amount"]
            for entry in income_data
            if datetime.strptime(entry["date"], "%Y-%m-%d").month == selected_month
            and datetime.strptime(entry["date"], "%Y-%m-%d").year == selected_year
        )

        total_expenses = sum(
            entry["amount"]
            for entry in expense_data
            if datetime.strptime(entry["date"], "%Y-%m-%d").month == selected_month
            and datetime.strptime(entry["date"], "%Y-%m-%d").year == selected_year
        )

        # Calculate net balance
        net_balance = total_income - total_expenses

        # Update labels
        total_income_label.config(text=f"Total Income: ${total_income:.2f}")
        total_expenses_label.config(text=f"Total Expenses: ${total_expenses:.2f}")
        net_balance_label.config(text=f"Net Balance: ${net_balance:.2f}")

    except Exception as e:
        messagebox.showerror("Error", f"Could not update summary: {e}")


# Create frames for each section
expense_frame = tk.LabelFrame(root, text="Add Expense", padx=10, pady=10)
income_frame = tk.LabelFrame(root, text="Add Income", padx=10, pady=10)
report_frame = tk.LabelFrame(root, text="Reports", padx=10, pady=10)
summary_frame = tk.LabelFrame(root, text="Quick Summary Dashboard", padx=10, pady=10)

# Expense fields
expense_amount_label = tk.Label(expense_frame, text="Amount")
expense_amount_label.grid(row=0, column=0)
expense_amount_entry = tk.Entry(expense_frame)
expense_amount_entry.grid(row=0, column=1)

expense_category_label = tk.Label(expense_frame, text="Category")
expense_category_label.grid(row=1, column=0)
expense_category_entry = tk.Entry(expense_frame)
expense_category_entry.grid(row=1, column=1)

expense_date_label = tk.Label(expense_frame, text="Date (YYYY-MM-DD)")
expense_date_label.grid(row=2, column=0)
expense_date_entry = tk.Entry(expense_frame)
expense_date_entry.grid(row=2, column=1)

expense_description_label = tk.Label(expense_frame, text="Description")
expense_description_label.grid(row=3, column=0)
expense_description_entry = tk.Entry(expense_frame)
expense_description_entry.grid(row=3, column=1)

expense_button = tk.Button(expense_frame, text="Add Expense", command=add_expense_gui)
expense_button.grid(row=4, column=0, columnspan=2)

# Income fields
income_amount_label = tk.Label(income_frame, text="Amount")
income_amount_label.grid(row=0, column=0)
income_amount_entry = tk.Entry(income_frame)
income_amount_entry.grid(row=0, column=1)

income_source_label = tk.Label(income_frame, text="Source")
income_source_label.grid(row=1, column=0)
income_source_entry = tk.Entry(income_frame)
income_source_entry.grid(row=1, column=1)

income_date_label = tk.Label(income_frame, text="Date (YYYY-MM-DD)")
income_date_label.grid(row=2, column=0)
income_date_entry = tk.Entry(income_frame)
income_date_entry.grid(row=2, column=1)

income_button = tk.Button(income_frame, text="Add Income", command=add_income_gui)
income_button.grid(row=3, column=0, columnspan=2)

# Report buttons
view_expenses_button = tk.Button(report_frame, text="View Expenses by Category", command=view_expenses_by_category_gui)
view_expenses_button.grid(row=0, column=0, columnspan=2)

year_label = tk.Label(report_frame, text="Year")
year_label.grid(row=1, column=0)
year_entry = tk.Entry(report_frame)
year_entry.grid(row=1, column=1)

month_label = tk.Label(report_frame, text="Month")
month_label.grid(row=2, column=0)
month_entry = tk.Entry(report_frame)
month_entry.grid(row=2, column=1)

view_income_expenses_button = tk.Button(report_frame, text="View Monthly Income vs Expenses", command=view_monthly_income_expenses_gui)
view_income_expenses_button.grid(row=3, column=0, columnspan=2)

# Add the "View Expenses" button in the expense frame
view_expenses_button = tk.Button(expense_frame, text="View Expenses", command=view_expenses_gui)
view_expenses_button.grid(row=5, column=0, columnspan=2)

# Add the "View Income" button in the income frame
view_income_button = tk.Button(income_frame, text="View Income", command=view_income_gui)
view_income_button.grid(row=4, column=0, columnspan=2)

total_income_label = tk.Label(summary_frame, text="Total Income: $0.00")
total_income_label.pack()

total_expenses_label = tk.Label(summary_frame, text="Total Expenses: $0.00")
total_expenses_label.pack()

net_balance_label = tk.Label(summary_frame, text="Net Balance: $0.00")
net_balance_label.pack()

month_label = tk.Label(summary_frame, text="Select Month")
month_label.pack(side="left", padx=5, pady=5)
month_var = tk.StringVar()
month_dropdown = tk.OptionMenu(summary_frame, month_var, *[str(i) for i in range(1, 13)])
month_var.set(str(datetime.now().month))  # Default to current month
month_dropdown.pack(side="left", padx=5, pady=5)

# Add dropdown for selecting year
year_label = tk.Label(summary_frame, text="Select Year")
year_label.pack(side="left", padx=5, pady=5)
year_var = tk.StringVar()
year_dropdown = tk.OptionMenu(summary_frame, year_var, *[str(i) for i in range(2020, 2031)])  # Example: years 2020-2030
year_var.set(str(datetime.now().year))  # Default to current year
year_dropdown.pack(side="left", padx=5, pady=5)

# Add button to update the summary
update_button = tk.Button(summary_frame, text="Update Summary", command=update_summary)
update_button.pack(padx=325, pady=10, side="left")

# Pack frames
summary_frame.pack(padx=10, pady=10, fill="both")
expense_frame.pack(padx=10, pady=10, fill="both")
income_frame.pack(padx=10, pady=10, fill="both")
report_frame.pack(padx=10, pady=10, fill="both")

# Run the main loop
update_summary()
root.mainloop()