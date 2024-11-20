from datetime import date
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List

class Expense(BaseModel):
    amount: float
    category: str
    date: date
    description: str

    def dict(self, *args, **kwargs):
        # Convert the date field to string in "YYYY-MM-DD" format
        expense_dict = super().dict(*args, **kwargs)
        expense_dict["date"] = expense_dict["date"].strftime("%Y-%m-%d")
        return expense_dict

class Income(BaseModel):
    amount: float
    source: str
    date: date

    def dict(self, *args, **kwargs):
        # Convert the date field to string in "YYYY-MM-DD" format
        income_dict = super().dict(*args, **kwargs)
        income_dict["date"] = income_dict["date"].strftime("%Y-%m-%d")
        return income_dict
