"""
test_validators.py
Unit tests for defensive input validation helper functions.
"""

import unittest
from src.models import ValidationError
from src.validators import (
    validate_category_name,
    validate_date_string,
    validate_menu_choice,
    validate_positive_amount,
)


class TestValidators(unittest.TestCase):
    def test_validate_positive_amount_valid(self):
        self.assertEqual(validate_positive_amount("250.50"), 250.50)
        self.assertEqual(validate_positive_amount("₹1,200.00"), 1200.00)
        self.assertEqual(validate_positive_amount(" 50 "), 50.0)

    def test_validate_positive_amount_invalid(self):
        with self.assertRaises(ValidationError):
            validate_positive_amount("-10")
        with self.assertRaises(ValidationError):
            validate_positive_amount("abc")
        with self.assertRaises(ValidationError):
            validate_positive_amount("")

    def test_validate_date_string_valid(self):
        self.assertEqual(validate_date_string("2026-10-15"), "2026-10-15")

    def test_validate_date_string_invalid(self):
        with self.assertRaises(ValidationError):
            validate_date_string("2026-02-31")
        with self.assertRaises(ValidationError):
            validate_date_string("15-10-2026")

    def test_validate_category_name(self):
        self.assertEqual(validate_category_name("  food  "), "Food")
        with self.assertRaises(ValidationError):
            validate_category_name("   ")

    def test_validate_menu_choice(self):
        self.assertEqual(validate_menu_choice("3", 0, 9), 3)
        with self.assertRaises(ValidationError):
            validate_menu_choice("10", 0, 9)
        with self.assertRaises(ValidationError):
            validate_menu_choice("x", 0, 9)


if __name__ == "__main__":
    unittest.main()
