import json
from models import Expense, Income
from typing import List
from datetime import datetime

DATA_FILE = "data.json"


def load_data():
    # Load data from the JSON file
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

            # Ensure all expenses and income dates are in datetime.date format
            for expense in data["expenses"]:
                if expense["amount"] == '':
                    expense["amount"] = 0.0  # Default to 0.0 if 'amount' is empty
                else:
                    try:
                        expense["amount"] = float(expense["amount"])
                    except ValueError:
                        expense["amount"] = 0.0  # Default to 0.0 if invalid value
                expense["date"] = datetime.fromisoformat(expense["date"]).date()

            for income in data["income"]:
                if income["amount"] == '':
                    income["amount"] = 0.0  # Default to 0.0 if 'amount' is empty
                else:
                    try:
                        income["amount"] = float(income["amount"])
                    except ValueError:
                        income["amount"] = 0.0  
                income["date"] = datetime.fromisoformat(income["date"]).date()

            return data
    except FileNotFoundError:
        return {"expenses": [], "income": []}
    except json.JSONDecodeError:
        print("Error: Data file is not in valid JSON format.")
        return {"expenses": [], "income": []}

def save_data(data):
    # Save data back to the JSON file
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, default=str, indent=4)


def clean_data(data):
    # Ensure the 'amount' field is a valid number
    for entry in data:
        if isinstance(entry.get('amount', ''), str) and entry['amount'] == '':
            entry['amount'] = 0  # Replace empty strings with 0 or another default
        try:
            entry['amount'] = float(entry['amount'])  # Convert to float
        except ValueError:
            entry['amount'] = 0  # Set to 0 if it fails to convert
    return data

def get_all_expenses():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
        return data.get("expenses", [])
    except FileNotFoundError:
        return []
    
def get_all_income():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
        return data.get("income", [])
    except FileNotFoundError:
        return []

def add_expense(expense: Expense):
    data = load_data()
    data["expenses"].append(expense.dict())
    save_data(data)

def add_income(income: Income):
    data = load_data()
    data["income"].append(income.dict())
    save_data(data)