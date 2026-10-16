import unittest
from datetime import date
from decimal import Decimal
from src.validators import (validate_department_name, validate_email, validate_hire_date,
                            validate_name, validate_phone, validate_positive_id, validate_salary)


class ValidatorTests(unittest.TestCase):
    def test_name_trims_whitespace(self):
        self.assertEqual(validate_name(" Maya Patel "), "Maya Patel")

    def test_name_rejects_empty(self):
        with self.assertRaises(ValueError):
            validate_name(" ")

    def test_email_normalizes_case(self):
        self.assertEqual(validate_email("USER@EXAMPLE.COM"), "user@example.com")

    def test_email_rejects_invalid(self):
        with self.assertRaises(ValueError):
            validate_email("bad-email")

    def test_phone_is_optional(self):
        self.assertIsNone(validate_phone(""))

    def test_salary_accepts_two_decimal_places(self):
        self.assertEqual(validate_salary("45000.50"), Decimal("45000.50"))

    def test_salary_rejects_negative(self):
        with self.assertRaises(ValueError):
            validate_salary("-10")

    def test_salary_rejects_extra_decimal_places(self):
        with self.assertRaises(ValueError):
            validate_salary("12.345")

    def test_hire_date_parses(self):
        self.assertEqual(validate_hire_date("2024-01-31"), date(2024, 1, 31))

    def test_hire_date_rejects_future(self):
        with self.assertRaises(ValueError):
            validate_hire_date(f"{date.today().year + 1}-01-01")

    def test_positive_id_rejects_zero(self):
        with self.assertRaises(ValueError):
            validate_positive_id("0")

    def test_department_name(self):
        self.assertEqual(validate_department_name("Customer Support"), "Customer Support")


if __name__ == "__main__":
    unittest.main()
