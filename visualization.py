import matplotlib.pyplot as plt
from collections import defaultdict
from data_handler import load_data
from datetime import datetime, date

def plot_expenses_by_category():
    data = load_data()
    expenses = data["expenses"]

    # Aggregate expenses by category
    category_totals = defaultdict(float)
    for expense in expenses:
        try:
            amount = float(expense["amount"]) if expense["amount"] else 0.0
        except ValueError:
            amount = 0.0 
        category_totals[expense["category"]] += amount

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    # Create a pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Expenses by Category")
    plt.show()

def plot_monthly_income_expenses(year: int, month: int):
    data = load_data()
    expenses = data["expenses"]
    income = data["income"]

    monthly_expenses = 0.0
    monthly_income = 0.0

    def ensure_date_string(date_value):
        if isinstance(date_value, str):
            return date_value
        elif isinstance(date_value, datetime):
            return date_value.strftime("%Y-%m-%d")
        elif isinstance(date_value, date):
            return date_value.isoformat()  
        else:
            raise ValueError(f"Invalid date type: {type(date_value)}")

    for expense in expenses:
        try:
            expense_date_str = ensure_date_string(expense["date"])
            expense_date = datetime.fromisoformat(expense_date_str).date()  
            if expense_date.year == year and expense_date.month == month:
                amount = float(expense["amount"]) if expense["amount"] else 0.0
                monthly_expenses += amount
        except ValueError as e:
            print(f"Error parsing expense date {expense['date']}: {e}")
        except KeyError as e:
            print(f"Missing expected key {e} in expense data.")

    # Filter income by month and year
    for inc in income:
        try:
            income_date_str = ensure_date_string(inc["date"])
            income_date = datetime.fromisoformat(income_date_str).date()  
            if income_date.year == year and income_date.month == month:
                amount = float(inc["amount"]) if inc["amount"] else 0.0
                monthly_income += amount
        except ValueError as e:
            print(f"Error parsing income date {inc['date']}: {e}")
        except KeyError as e:
            print(f"Missing expected key {e} in income data.")

    print(f"Monthly Expenses for {year}-{month}: {monthly_expenses}")
    print(f"Monthly Income for {year}-{month}: {monthly_income}")

    if monthly_income == 0 and monthly_expenses == 0:
        print("No data available for this month.")
    else:
        plt.figure(figsize=(6, 4))
        plt.bar(["Income", "Expenses"], [monthly_income, monthly_expenses], color=["green", "red"])
        plt.title(f"Income vs. Expenses for {year}-{month:02}")
        plt.ylabel("Amount")
        plt.show()
