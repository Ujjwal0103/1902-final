from datetime import datetime
from models import Expense, Income
from data_handler import add_expense, add_income, save_data
from visualization import plot_expenses_by_category, plot_monthly_income_expenses
import atexit

# This will reset the data when the program ends
def reset_data_on_exit():
    initial_data = {"expenses": [], "income": []}
    save_data(initial_data)  # Save empty data to reset the file

# Register the function to run at exit
atexit.register(reset_data_on_exit)

def add_expense_ui():
    amount = float(input("Enter expense amount: "))
    category = input("Enter category (e.g., Food, Rent): ")
    date_str = input("Enter date (YYYY-MM-DD): ")
    description = input("Enter description: ")
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    expense = Expense(amount=amount, category=category, date=date, description=description)
    add_expense(expense)
    print("Expense added successfully.")

def add_income_ui():
    amount = float(input("Enter income amount: "))
    source = input("Enter income source: ")
    date_str = input("Enter date (YYYY-MM-DD): ")
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    income = Income(amount=amount, source=source, date=date)
    add_income(income)
    print("Income added successfully.")

def main():
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Expense")
        print("2. Add Income")
        print("3. View Expenses by Category")
        print("4. View Monthly Income vs Expenses")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_expense_ui()
        elif choice == "2":
            add_income_ui()
        elif choice == "3":
            plot_expenses_by_category()
        elif choice == "4":
            year = int(input("Enter year (e.g., 2023): "))
            month = int(input("Enter month (e.g., 5 for May): "))
            plot_monthly_income_expenses(year, month)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")
if __name__ == "__main__":
    main()
