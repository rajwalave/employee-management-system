CREATE DATABASE IF NOT EXISTS employee_management
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE employee_management;

CREATE TABLE IF NOT EXISTS departments (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(255) NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_departments_name (name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS employees (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(80) NOT NULL,
  last_name VARCHAR(80) NOT NULL,
  email VARCHAR(254) NOT NULL,
  phone VARCHAR(30) NULL,
  department_id INT UNSIGNED NOT NULL,
  hire_date DATE NOT NULL,
  salary DECIMAL(12,2) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_employees_email (email),
  KEY idx_employees_name (last_name, first_name),
  KEY idx_employees_department (department_id),
  KEY idx_employees_hire_date (hire_date),
  CONSTRAINT fk_employees_department FOREIGN KEY (department_id)
    REFERENCES departments(id) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT chk_employees_salary CHECK (salary >= 0)
) ENGINE=InnoDB;

INSERT IGNORE INTO departments (name, description) VALUES
 ('Human Resources', 'Recruitment and employee support'),
 ('Engineering', 'Software and technology'),
 ('Finance', 'Accounting and financial reporting'),
 ('Sales', 'Customer relationships and sales operations');
