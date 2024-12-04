from datetime import date
from pydantic import BaseModel

class Expense(BaseModel):
    amount: float
    category: str
    date: date
    description: str

    def dict(self, *args, **kwargs):
        expense_dict = super().dict(*args, **kwargs)
        expense_dict["date"] = expense_dict["date"].strftime("%Y-%m-%d")
        return expense_dict

class Income(BaseModel):
    amount: float
    source: str
    date: date

    def dict(self, *args, **kwargs):
        income_dict = super().dict(*args, **kwargs)
        income_dict["date"] = income_dict["date"].strftime("%Y-%m-%d")
        return income_dict
