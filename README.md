# Employee Management System | Python + MySQL

A command-line Employee Management System for managing employee records, departments, and salary information.

## Features
- Employee CRUD: create, list/search, update, and delete
- Department management
- Salary and department reports
- Input validation and user-friendly error handling
- Parameterized SQL queries
- MySQL foreign keys and indexes
- Unit tests for validators

## Requirements
- Python 3.10+
- MySQL Server 8.0+
- pip

## Setup

1. Extract this project and open a terminal in its folder.
2. Run `database/schema.sql` in MySQL Workbench, or:
   ```bash
   mysql -u root -p < database/schema.sql
   ```
3. Create and activate a virtual environment (recommended), then install dependencies:
   ```bash
   python -m venv .venv
   ```
   Windows PowerShell:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   macOS/Linux:
   ```bash
   source .venv/bin/activate
   ```
   Then:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and enter your local MySQL connection settings:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD= ****
   DB_NAME=employee_management
   ```
5. Start the app:
   ```bash
   python main.py
   ```

## Tests
The validator tests do not need a running MySQL server:
```bash
python -m unittest discover -s tests -v
```

## Database design
- `departments`: unique department names and optional descriptions
- `employees`: contact details, department, hire date, and salary
- Indexes support common employee-name, department, and hire-date searches

## GitHub details
**Suggested repository name:** `employee-management-system`

**Suggested description:** Employee Management System built with Python and MySQL, featuring employee and department CRUD operations, input validation, exception handling, and salary reporting.

## Security and project notes
- Do not commit `.env` or real credentials. `.gitignore` excludes it.
- Queries use parameters rather than string concatenation.
- This is a portfolio/demo application. Add authentication, authorization, and audit logging before using real employee data.
- Review, run, and understand the project before presenting it in a portfolio.
