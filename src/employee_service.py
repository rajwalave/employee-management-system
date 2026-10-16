"""Employee and department database operations and reports."""
from mysql.connector import Error, IntegrityError
from src.database import get_connection


class EmployeeServiceError(Exception):
    """Raised when a database operation cannot be completed."""


class EmployeeService:
    def add_department(self, name, description=None):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO departments (name, description) VALUES (%s, %s)",
                                (name, description or None))
                    conn.commit()
                    return cur.lastrowid
        except IntegrityError as exc:
            raise EmployeeServiceError("That department name already exists.") from exc
        except Error as exc:
            raise EmployeeServiceError(f"Could not add department: {exc}") from exc

    def list_departments(self):
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    cur.execute("SELECT id, name, description FROM departments ORDER BY name")
                    return cur.fetchall()
        except Error as exc:
            raise EmployeeServiceError(f"Could not list departments: {exc}") from exc

    def add_employee(self, employee):
        sql = """INSERT INTO employees
        (first_name, last_name, email, phone, department_id, hire_date, salary)
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (employee["first_name"], employee["last_name"],
                        employee["email"], employee.get("phone"), employee["department_id"],
                        employee["hire_date"], employee["salary"]))
                    conn.commit()
                    return cur.lastrowid
        except IntegrityError as exc:
            message = str(exc).lower()
            if "email" in message:
                raise EmployeeServiceError("An employee with that email already exists.") from exc
            if "department" in message:
                raise EmployeeServiceError("Choose an existing department.") from exc
            raise EmployeeServiceError(f"Data constraint failed: {exc}") from exc
        except Error as exc:
            raise EmployeeServiceError(f"Could not add employee: {exc}") from exc

    def list_employees(self, search=None):
        sql = """SELECT e.id, e.first_name, e.last_name, e.email, e.phone,
        e.department_id, d.name AS department, e.hire_date, e.salary
        FROM employees e JOIN departments d ON d.id=e.department_id"""
        params = ()
        if search:
            sql += " WHERE e.first_name LIKE %s OR e.last_name LIKE %s OR e.email LIKE %s"
            term = f"%{search.strip()}%"
            params = (term, term, term)
        sql += " ORDER BY e.last_name, e.first_name, e.id"
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    cur.execute(sql, params)
                    return cur.fetchall()
        except Error as exc:
            raise EmployeeServiceError(f"Could not retrieve employees: {exc}") from exc

    def get_employee(self, employee_id):
        sql = """SELECT e.id, e.first_name, e.last_name, e.email, e.phone,
        e.department_id, d.name AS department, e.hire_date, e.salary
        FROM employees e JOIN departments d ON d.id=e.department_id WHERE e.id=%s"""
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    cur.execute(sql, (employee_id,))
                    return cur.fetchone()
        except Error as exc:
            raise EmployeeServiceError(f"Could not retrieve employee: {exc}") from exc

    def update_employee(self, employee_id, employee):
        sql = """UPDATE employees SET first_name=%s, last_name=%s, email=%s, phone=%s,
        department_id=%s, hire_date=%s, salary=%s WHERE id=%s"""
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (employee["first_name"], employee["last_name"],
                        employee["email"], employee.get("phone"), employee["department_id"],
                        employee["hire_date"], employee["salary"], employee_id))
                    conn.commit()
                    return cur.rowcount > 0
        except IntegrityError as exc:
            if "email" in str(exc).lower():
                raise EmployeeServiceError("An employee with that email already exists.") from exc
            raise EmployeeServiceError(f"Data constraint failed: {exc}") from exc
        except Error as exc:
            raise EmployeeServiceError(f"Could not update employee: {exc}") from exc

    def delete_employee(self, employee_id):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM employees WHERE id=%s", (employee_id,))
                    conn.commit()
                    return cur.rowcount > 0
        except Error as exc:
            raise EmployeeServiceError(f"Could not delete employee: {exc}") from exc

    def employees_by_department(self):
        sql = """SELECT d.name AS department, COUNT(e.id) AS employee_count,
        COALESCE(ROUND(AVG(e.salary), 2), 0) AS average_salary,
        COALESCE(ROUND(SUM(e.salary), 2), 0) AS total_salary
        FROM departments d LEFT JOIN employees e ON e.department_id=d.id
        GROUP BY d.id, d.name ORDER BY d.name"""
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    cur.execute(sql)
                    return cur.fetchall()
        except Error as exc:
            raise EmployeeServiceError(f"Could not generate department report: {exc}") from exc

    def salary_summary(self):
        sql = """SELECT COUNT(*) AS employee_count,
        COALESCE(ROUND(AVG(salary), 2), 0) AS average_salary,
        COALESCE(ROUND(MIN(salary), 2), 0) AS minimum_salary,
        COALESCE(ROUND(MAX(salary), 2), 0) AS maximum_salary,
        COALESCE(ROUND(SUM(salary), 2), 0) AS total_monthly_salary FROM employees"""
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    cur.execute(sql)
                    return cur.fetchone()
        except Error as exc:
            raise EmployeeServiceError(f"Could not generate salary summary: {exc}") from exc

    def highest_paid_employees(self, limit=5):
        if not 1 <= limit <= 100:
            raise ValueError("Limit must be between 1 and 100.")
        sql = """SELECT e.id, CONCAT(e.first_name, ' ', e.last_name) AS employee,
        e.salary, d.name AS department FROM employees e
        JOIN departments d ON d.id=e.department_id
        ORDER BY e.salary DESC, e.last_name, e.first_name LIMIT %s"""
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    cur.execute(sql, (limit,))
                    return cur.fetchall()
        except Error as exc:
            raise EmployeeServiceError(f"Could not generate salary ranking: {exc}") from exc
