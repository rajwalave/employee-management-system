"""Interactive command-line interface."""
from datetime import date
from mysql.connector import Error
from src.database import test_connection
from src.employee_service import EmployeeService, EmployeeServiceError
from src.validators import (validate_department_name, validate_email, validate_hire_date,
    validate_name, validate_phone, validate_positive_id, validate_salary)

service = EmployeeService()


def ask(label, validator, allow_blank=False, default=None):
    while True:
        raw = input(f"{label}" + (f" [{default}]" if default is not None else "") + ": ").strip()
        if allow_blank and raw == "":
            return default
        try:
            return validator(raw)
        except ValueError as exc:
            print(f"Invalid input: {exc}")


def choose_department(existing_id=None):
    departments = service.list_departments()
    if not departments:
        raise EmployeeServiceError("No departments found. Add a department first.")
    print("\nDepartments:")
    for dept in departments:
        print(f"  {dept['id']}: {dept['name']}")
    if existing_id is not None:
        raw = input(f"Department ID [{existing_id}] (Enter to keep): ").strip()
        if not raw:
            return existing_id
        return validate_positive_id(raw, "Department ID")
    return ask("Department ID", lambda value: validate_positive_id(value, "Department ID"))


def collect_employee(existing=None):
    existing = existing or {}
    first = ask("First name", lambda v: validate_name(v, "First name"),
                bool(existing), existing.get("first_name"))
    last = ask("Last name", lambda v: validate_name(v, "Last name"),
               bool(existing), existing.get("last_name"))
    email = ask("Email", validate_email, bool(existing), existing.get("email"))
    phone = ask("Phone (optional)", validate_phone, bool(existing), existing.get("phone") or "")
    department_id = choose_department(existing.get("department_id"))
    hire_date = ask("Hire date (YYYY-MM-DD)", validate_hire_date, bool(existing),
                    str(existing.get("hire_date") or date.today()))
    salary = ask("Salary", validate_salary, bool(existing), str(existing.get("salary") or ""))
    return {"first_name": first, "last_name": last, "email": email, "phone": phone,
            "department_id": department_id, "hire_date": hire_date, "salary": salary}


def print_table(rows, columns):
    if not rows:
        print("No records found.")
        return
    widths = {key: max(len(title), *(len(str(row.get(key, ""))) for row in rows))
              for key, title in columns}
    print(" | ".join(title.ljust(widths[key]) for key, title in columns))
    print("-+-".join("-" * widths[key] for key, _ in columns))
    for row in rows:
        print(" | ".join(str(row.get(key, "")).ljust(widths[key]) for key, _ in columns))


def add_employee():
    employee_id = service.add_employee(collect_employee())
    print(f"Employee added successfully. ID: {employee_id}")


def list_employees():
    term = input("Search by name/email (Enter for all): ").strip()
    print_table(service.list_employees(term or None), [
        ("id", "ID"), ("first_name", "First"), ("last_name", "Last"),
        ("email", "Email"), ("department", "Department"),
        ("hire_date", "Hire date"), ("salary", "Salary")])


def update_employee():
    employee_id = ask("Employee ID to update", validate_positive_id)
    existing = service.get_employee(employee_id)
    if not existing:
        print("Employee not found.")
        return
    print("Press Enter to keep the current value.")
    if service.update_employee(employee_id, collect_employee(existing)):
        print("Employee updated successfully.")
    else:
        print("No changes saved; employee may not exist.")


def delete_employee():
    employee_id = ask("Employee ID to delete", validate_positive_id)
    employee = service.get_employee(employee_id)
    if not employee:
        print("Employee not found.")
        return
    answer = input(f"Delete {employee['first_name']} {employee['last_name']} (y/N)? ").strip().lower()
    if answer == "y":
        print("Employee deleted." if service.delete_employee(employee_id) else "Employee not deleted.")
    else:
        print("Deletion cancelled.")


def add_department():
    name = ask("Department name", validate_department_name)
    description = input("Description (optional): ").strip() or None
    print(f"Department added. ID: {service.add_department(name, description)}")


def list_departments():
    print_table(service.list_departments(), [
        ("id", "ID"), ("name", "Department"), ("description", "Description")])


def reports():
    print("\nEmployees by department")
    print_table(service.employees_by_department(), [
        ("department", "Department"), ("employee_count", "Employees"),
        ("average_salary", "Average salary"), ("total_salary", "Total salary")])
    print("\nSalary summary")
    for label, key in [("Employee count", "employee_count"),
        ("Average salary", "average_salary"), ("Minimum salary", "minimum_salary"),
        ("Maximum salary", "maximum_salary"), ("Total monthly salary", "total_monthly_salary")]:
        print(f"  {label}: {service.salary_summary()[key]}")
    print("\nHighest-paid employees")
    print_table(service.highest_paid_employees(), [
        ("id", "ID"), ("employee", "Employee"), ("department", "Department"), ("salary", "Salary")])


def main():
    ok, message = test_connection()
    if not ok:
        print(f"Database connection failed: {message}")
        print("Check MySQL is running, run database/schema.sql, and configure .env.")
        return
    print(f"Employee Management System — {message}")
    actions = {
        "1": ("Add employee", add_employee),
        "2": ("List/search employees", list_employees),
        "3": ("Update employee", update_employee),
        "4": ("Delete employee", delete_employee),
        "5": ("Add department", add_department),
        "6": ("List departments", list_departments),
        "7": ("View reports", reports),
    }
    while True:
        print("\n" + "=" * 34)
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            return
        if choice not in actions:
            print("Choose a valid menu option.")
            continue
        try:
            actions[choice][1]()
        except (EmployeeServiceError, ValueError) as exc:
            print(f"Error: {exc}")
        except (Error, RuntimeError) as exc:
            print(f"Database/configuration error: {exc}")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            return
