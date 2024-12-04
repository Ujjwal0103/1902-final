import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from data_handler import add_expense, add_income, save_data, get_all_income, get_all_expenses
from models import Expense, Income
from visualization import plot_expenses_by_category, plot_monthly_income_expenses

BACKGROUND_COLOR = "#f0f4f8"
PRIMARY_COLOR = "#4a90e2"
SECONDARY_COLOR = "#7ed6df"
TEXT_COLOR = "#2c3e50"
ACCENT_COLOR = "#3498db"

# Initialize main window
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("500x1000")
root.configure(bg=BACKGROUND_COLOR)

style = ttk.Style()
style.theme_use('clam')
style.configure("TFrame", background=BACKGROUND_COLOR)
style.configure("TLabel", 
                background=BACKGROUND_COLOR, 
                foreground=TEXT_COLOR, 
                font=("Segoe UI", 10))
style.configure("TButton", 
                background=PRIMARY_COLOR, 
                foreground="white", 
                font=("Segoe UI", 10, "bold"))

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
    save_data(initial_data) 
    root.destroy() 

root.protocol("WM_DELETE_WINDOW", reset_data_on_exit)

def create_styled_frame(parent, title):
    frame = ttk.Frame(parent, style="TFrame")
    frame.pack(padx=15, pady=0, fill="x")
    
    title_label = ttk.Label(frame, text=title, 
                            font=("Segoe UI", 12, "bold"), 
                            foreground=PRIMARY_COLOR)
    title_label.pack(pady=(0, 0))
    
    separator = ttk.Separator(frame, orient='horizontal')
    separator.pack(fill='x', padx=10, pady=(0, 0))
    
    return frame

def view_expenses_gui():
    try:
        view_window = tk.Toplevel(root)
        view_window.title("View and Delete Expenses")
        view_window.geometry("400x300")

        expenses_frame = tk.Frame(view_window)
        expenses_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(expenses_frame)
        scrollbar.pack(side="right", fill="y")

        expenses_listbox = tk.Listbox(expenses_frame, yscrollcommand=scrollbar.set, width=50, height=15)
        expenses_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=expenses_listbox.yview)

        expenses = get_all_expenses()
        income = get_all_income()
        for i, expense in enumerate(expenses):
            expenses_listbox.insert(tk.END, f"{i + 1}. {expense['description']} - ${expense['amount']} ({expense['category']}) on {expense['date']}")

        def delete_selected_expense():
            try:
                selected_index = expenses_listbox.curselection()
                if not selected_index:
                    raise Exception("No expense selected")
                selected_index = selected_index[0] 
                del expenses[selected_index]  
                save_data({"expenses": expenses, "income": income})  
                expenses_listbox.delete(selected_index)  
                messagebox.showinfo("Success", "Expense deleted successfully!")
                update_summary()
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete expense: {e}")

        delete_button = tk.Button(view_window, text="Delete Selected Expense", command=delete_selected_expense)
        delete_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Could not load expenses: {e}")


def view_income_gui():
    try:
        view_window = tk.Toplevel(root)
        view_window.title("View and Delete Income")
        view_window.geometry("400x300")

        income_frame = tk.Frame(view_window)
        income_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(income_frame)
        scrollbar.pack(side="right", fill="y")

        income_listbox = tk.Listbox(income_frame, yscrollcommand=scrollbar.set, width=50, height=15)
        income_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=income_listbox.yview)

        income_data = get_all_income()
        expenses = get_all_expenses()
        for i, income in enumerate(income_data):
            income_listbox.insert(
                tk.END, f"{i + 1}. {income['source']} - ${income['amount']} on {income['date']}"
            )

        def delete_selected_income():
            try:
                selected_index = income_listbox.curselection()
                if not selected_index:
                    raise Exception("No income selected")
                selected_index = selected_index[0]  
                del income_data[selected_index]  
                save_data({"expenses": expenses, "income": income_data}) 
                income_listbox.delete(selected_index) 
                messagebox.showinfo("Success", "Income deleted successfully!")
                update_summary()
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete income: {e}")

        delete_button = tk.Button(view_window, text="Delete Selected Income", command=delete_selected_income)
        delete_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Could not load income: {e}")

def update_summary():
    try:
        income_data = get_all_income()
        expense_data = get_all_expenses()

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

        net_balance = total_income - total_expenses

        total_income_label.config(text=f"Total Income: ${total_income:.2f}", font=24)
        total_expenses_label.config(text=f"Total Expenses: ${total_expenses:.2f}", font=24)
        net_balance_label.config(text=f"Net Balance: ${net_balance:.2f}", font=24)

    except Exception as e:
        messagebox.showerror("Error", f"Could not update summary: {e}")

summary_frame = create_styled_frame(root, "Quick Summary Dashboard")

total_income_label = ttk.Label(summary_frame, text="Total Income: $0.00")
total_income_label.pack(pady=2)

total_expenses_label = ttk.Label(summary_frame, text="Total Expenses: $0.00")
total_expenses_label.pack(pady=2)

net_balance_label = ttk.Label(summary_frame, text="Net Balance: $0.00")
net_balance_label.pack(pady=2)

month_label = ttk.Label(summary_frame, text="Select Month", font= 24)
month_label.pack(side="left", padx=5, pady=2)
month_var = tk.StringVar()
month_dropdown = ttk.OptionMenu(summary_frame, month_var, *[str(i) for i in range(0, 13)])
month_dropdown.config(width=5)
month_var.set(str(datetime.now().month)) 
month_dropdown.pack(side="left", padx=5, pady=2)
year_label = ttk.Label(summary_frame, text="Select Year", font= 24)
year_label.pack(side="left", padx=5, pady=2)
year_var = tk.StringVar()
year_dropdown = ttk.OptionMenu(summary_frame, year_var, *[str(i) for i in range(2020, 2031)])
year_dropdown.config(width=5)
year_var.set(str(datetime.now().year))  
year_dropdown.pack(side="left", padx=5, pady=2)

update_button = ttk.Button(summary_frame, text="Update Summary", command=update_summary, width=50)
update_button.pack(side = "left", padx=5, pady=2)

# Expense fields

expense_frame = create_styled_frame(root, "Add Expense")
expense_amount_label = ttk.Label(expense_frame, text="Amount")
expense_amount_label.pack(fill='x', padx=20, pady=(2, 0))
expense_amount_entry = ttk.Entry(expense_frame, width=40)
expense_amount_entry.pack(fill='x', padx=20, pady=(2, 5))

expense_category_label = ttk.Label(expense_frame, text="Category")
expense_category_label.pack(fill='x', padx=20, pady=(2, 0))
expense_category_entry = ttk.Entry(expense_frame, width=40)
expense_category_entry.pack(fill='x', padx=20, pady=(0, 2))

expense_date_label = ttk.Label(expense_frame, text="Date (YYYY-MM-DD)")
expense_date_label.pack(fill='x', padx=20, pady=(2, 0))
expense_date_entry = ttk.Entry(expense_frame, width=40)
expense_date_entry.pack(fill='x', padx=20, pady=(0, 2))

expense_description_label = ttk.Label(expense_frame, text="Description")
expense_description_label.pack(fill='x', padx=20, pady=(2, 0))
expense_description_entry = ttk.Entry(expense_frame, width=40)
expense_description_entry.pack(fill='x', padx=20, pady=(0, 2))

expense_button = ttk.Button(expense_frame, text="Add Expense", command=add_expense_gui, )
expense_button.pack(pady=2)

view_expenses_button = ttk.Button(expense_frame, text="View Expenses", command=view_expenses_gui)
view_expenses_button.pack(pady=2)

# Income frame
income_frame = create_styled_frame(root, "Add Income")

income_amount_label = ttk.Label(income_frame, text="Amount")
income_amount_label.pack(fill='x', padx=20, pady=(2, 0))
income_amount_entry = ttk.Entry(income_frame, width=40)
income_amount_entry.pack(fill='x', padx=20, pady=(0, 2))

income_source_label = ttk.Label(income_frame, text="Source")
income_source_label.pack(fill='x', padx=20, pady=(2, 0))
income_source_entry = ttk.Entry(income_frame, width=40)
income_source_entry.pack(fill='x', padx=20, pady=(0, 2))

income_date_label = ttk.Label(income_frame, text="Date (YYYY-MM-DD)")
income_date_label.pack(fill='x', padx=20, pady=(2, 0))
income_date_entry = ttk.Entry(income_frame, width=40)
income_date_entry.pack(fill='x', padx=20, pady=(0, 2))

income_button = ttk.Button(income_frame, text="Add Income", command=add_income_gui)
income_button.pack(pady=2)

view_income_button = ttk.Button(income_frame, text="View Income", command=view_income_gui)
view_income_button.pack(pady=2)

# Report frame
report_frame = create_styled_frame(root, "Reports")

view_expenses_by_category_button = ttk.Button(report_frame, text="View Expenses by Category", command=view_expenses_by_category_gui)
view_expenses_by_category_button.pack(fill='x', padx=20, pady=5)

year_label = ttk.Label(report_frame, text="Year")
year_label.pack(fill='x', padx=20, pady=(2, 0))
year_entry = ttk.Entry(report_frame, width=40)
year_entry.pack(fill='x', padx=20, pady=(0, 2))

month_label = ttk.Label(report_frame, text="Month")
month_label.pack(fill='x', padx=20, pady=(2, 0))
month_entry = ttk.Entry(report_frame, width=40)
month_entry.pack(fill='x', padx=20, pady=(0, 2))

view_income_expenses_button = ttk.Button(report_frame, text="View Monthly Income vs Expenses", command=view_monthly_income_expenses_gui)
view_income_expenses_button.pack(fill='x', padx=20, pady=2)

# Pack frames
summary_frame.pack(padx=10, pady=5, fill="both")
expense_frame.pack(padx=10, pady=5, fill="both")
income_frame.pack(padx=10, pady=5, fill="both")
report_frame.pack(padx=10, pady=5, fill="both")


update_summary()
root.mainloop()
