from enum import Enum


class RecordType(str, Enum):
    income = "income"
    expense = "expense"
