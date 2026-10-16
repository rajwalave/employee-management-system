"""Input validation helpers."""
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
import re


def validate_name(value, field="Name"):
    value = (value or "").strip()
    if not value:
        raise ValueError(f"{field} is required.")
    if len(value) > 80:
        raise ValueError(f"{field} must be 80 characters or fewer.")
    if not re.fullmatch(r"[A-Za-z][A-Za-z .'-]*", value):
        raise ValueError(f"{field} may contain letters, spaces, apostrophes, periods, and hyphens.")
    return value


def validate_email(value):
    value = (value or "").strip().lower()
    if len(value) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value):
        raise ValueError("Enter a valid email address.")
    return value


def validate_phone(value):
    value = (value or "").strip()
    if not value:
        return None
    if not re.fullmatch(r"[+()0-9 .-]{7,30}", value):
        raise ValueError("Phone may contain digits, spaces, +, -, ., or parentheses.")
    digits = re.sub(r"\D", "", value)
    if not 7 <= len(digits) <= 15:
        raise ValueError("Phone number must contain 7–15 digits.")
    return value


def validate_salary(value):
    try:
        salary = Decimal(str(value).strip())
    except (InvalidOperation, AttributeError) as exc:
        raise ValueError("Salary must be a valid number.") from exc
    if not salary.is_finite() or salary < 0:
        raise ValueError("Salary must be a non-negative number.")
    if salary.as_tuple().exponent < -2:
        raise ValueError("Salary may have at most two decimal places.")
    if salary > Decimal("9999999999.99"):
        raise ValueError("Salary is too large.")
    return salary.quantize(Decimal("0.01"))


def validate_hire_date(value):
    try:
        parsed = datetime.strptime((value or "").strip(), "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError("Hire date must use YYYY-MM-DD format.") from exc
    if parsed > date.today():
        raise ValueError("Hire date cannot be in the future.")
    return parsed


def validate_positive_id(value, field="ID"):
    try:
        parsed = int(str(value).strip())
    except (ValueError, TypeError) as exc:
        raise ValueError(f"{field} must be a whole number.") from exc
    if parsed <= 0:
        raise ValueError(f"{field} must be greater than zero.")
    return parsed


def validate_department_name(value):
    value = (value or "").strip()
    if not value:
        raise ValueError("Department name is required.")
    if len(value) > 100:
        raise ValueError("Department name must be 100 characters or fewer.")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 &().'-]*", value):
        raise ValueError("Department name contains unsupported characters.")
    return value
