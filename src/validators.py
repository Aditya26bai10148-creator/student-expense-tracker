"""
validators.py
Defensive input validation functions for PySpend.
Ensures invalid user inputs are caught before reaching core business logic.
"""

from datetime import datetime
from src.models import ValidationError


def validate_positive_amount(amount_input: str) -> float:
    """
    Parses and validates a monetary string input.
    Must be a strictly positive number (float or int).
    """
    cleaned = str(amount_input).strip().replace("₹", "").replace(",", "")
    if not cleaned:
        raise ValidationError("Amount cannot be empty. Please enter a valid number.")

    try:
        amount = float(cleaned)
    except ValueError:
        raise ValidationError(f"Invalid monetary format '{amount_input}'. Please enter digits (e.g. 250 or 49.50).")

    if amount <= 0:
        raise ValidationError(f"Amount must be strictly greater than 0, got: {amount}")

    return round(amount, 2)


def validate_date_string(date_input: str) -> str:
    """
    Validates a date string in YYYY-MM-DD format.
    If input is empty, returns today's date formatted as YYYY-MM-DD.
    """
    cleaned = str(date_input).strip()
    if not cleaned:
        return datetime.now().strftime("%Y-%m-%d")

    try:
        parsed = datetime.strptime(cleaned, "%Y-%m-%d")
        return parsed.strftime("%Y-%m-%d")
    except ValueError:
        raise ValidationError(f"Invalid date format '{date_input}'. Required format is YYYY-MM-DD (e.g. 2026-10-05).")


def validate_category_name(category_input: str) -> str:
    """
    Validates and cleans a category name.
    """
    cleaned = str(category_input).strip().title()
    if not cleaned:
        raise ValidationError("Category name cannot be empty.")
    if len(cleaned) > 30:
        raise ValidationError("Category name is too long (maximum 30 characters).")
    return cleaned


def validate_menu_choice(choice_input: str, min_val: int, max_val: int) -> int:
    """
    Validates that a menu selection is an integer within [min_val, max_val].
    """
    cleaned = str(choice_input).strip()
    if not cleaned.isdigit():
        raise ValidationError(f"Invalid choice '{choice_input}'. Please enter a number between {min_val} and {max_val}.")
    
    val = int(cleaned)
    if val < min_val or val > max_val:
        raise ValidationError(f"Choice {val} is out of range ({min_val}-{max_val}).")
    
    return val
