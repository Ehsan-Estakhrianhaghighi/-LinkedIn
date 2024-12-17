-- Create the database
CREATE DATABASE company_db;

-- Connect to the database
USE company_db;

-- Create tables
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    location VARCHAR(50)
);

CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE salaries (
    salary_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    amount DECIMAL(10, 2),
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- Insert data into departments table
INSERT INTO departments (name, location) VALUES
('Engineering', 'New York'),
('Marketing', 'San Francisco'),
('Sales', 'Chicago'),
('HR', 'Boston'),
('Finance', 'Dallas'),
('IT', 'Seattle'),
('Customer Support', 'Austin'),
('Legal', 'Denver'),
('Operations', 'Los Angeles'),
('Admin', 'Miami'),
('R&D', 'Houston'),
('Procurement', 'Phoenix'),
('Quality Assurance', 'Philadelphia'),
('Supply Chain', 'San Diego'),
('Product Management', 'Las Vegas');

-- Insert data into employees table
INSERT INTO employees (first_name, last_name, department_id) VALUES
('John', 'Doe', 1),
('Jane', 'Smith', 2),
('Emily', 'Davis', 3),
('Michael', 'Brown', 1),
('Jessica', 'Jones', 2),
('Daniel', 'Garcia', 4),
('Laura', 'Martinez', 5),
('Kevin', 'Anderson', 6),
('Sarah', 'Taylor', 7),
('David', 'Thomas', 8),
('Michelle', 'Hernandez', 9),
('Chris', 'Moore', 10),
('Amanda', 'Jackson', 11),
('Brian', 'White', 12),
('Nicole', 'Harris', 13),
('Eric', 'Clark', 14),
('Kimberly', 'Lewis', 15);

-- Insert data into salaries table
INSERT INTO salaries (employee_id, amount, start_date, end_date) VALUES
(1, 70000, '2021-01-01', '2022-01-01'),
(2, 80000, '2021-02-01', '2022-02-01'),
(3, 75000, '2021-03-01', '2022-03-01'),
(4, 90000, '2021-04-01', '2022-04-01'),
(5, 65000, '2021-05-01', '2022-05-01'),
(6, 72000, '2021-06-01', '2022-06-01'),
(7, 67000, '2021-07-01', '2022-07-01'),
(8, 85000, '2021-08-01', '2022-08-01'),
(9, 92000, '2021-09-01', '2022-09-01'),
(10, 60000, '2021-10-01', '2022-10-01'),
(11, 71000, '2021-11-01', '2022-11-01'),
(12, 74000, '2021-12-01', '2022-12-01'),
(13, 78000, '2022-01-01', '2023-01-01'),
(14, 79000, '2022-02-01', '2023-02-01'),
(15, 81000, '2022-03-01', '2023-03-01'),
(16, 85000, '2022-04-01', '2023-04-01'),
(17, 88000, '2022-05-01', '2023-05-01');

-- Create indexes
CREATE INDEX idx_department_name ON departments(name);
CREATE INDEX idx_employee_name ON employees(first_name, last_name);
CREATE INDEX idx_salary_amount ON salaries(amount);

-- Create views
CREATE VIEW employee_salaries AS
SELECT e.first_name, e.last_name, d.name as department, s.amount
FROM employees e
JOIN departments d ON e.department_id = d.department_id
JOIN salaries s ON e.employee_id = s.employee_id;

-- Create temporary tables
CREATE TEMPORARY TABLE temp_high_salaries AS
SELECT e.first_name, e.last_name, s.amount
FROM employees e
JOIN salaries s ON e.employee_id = s.employee_id
WHERE s.amount > 75000;

-- Create triggers
CREATE TABLE salary_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    old_salary DECIMAL(10, 2),
    new_salary DECIMAL(10, 2),
    change_date TIMESTAMP
);

DELIMITER //

CREATE TRIGGER salary_update
AFTER UPDATE ON salaries
FOR EACH ROW
BEGIN
    IF OLD.amount <> NEW.amount THEN
        INSERT INTO salary_log (employee_id, old_salary, new_salary, change_date)
        VALUES (NEW.employee_id, OLD.amount, NEW.amount, NOW());
    END IF;
END;
//

DELIMITER ;

-- update the salaries table to see if it will be shown in the salary_log table
SELECT * FROM salaries WHERE employee_id = 1;

UPDATE salaries
SET amount = 73000
WHERE employee_id = 1;

SELECT * FROM salaries WHERE employee_id = 1;



-- Create stored procedures
DELIMITER //

CREATE PROCEDURE raise_salary(IN emp_id INT, IN increment DECIMAL(10, 2))
BEGIN
    UPDATE salaries
    SET amount = amount + increment
    WHERE employee_id = emp_id;
END;
//

DELIMITER ;

-- Run the procedures to see how it works
SELECT * FROM salaries WHERE employee_id = 2;
CALL raise_salary(2, 5000);
SELECT * FROM salaries WHERE employee_id = 2;

-- Create functions
DELIMITER //

CREATE FUNCTION get_employee_department(emp_id INT) RETURNS VARCHAR(50)
READS SQL DATA
BEGIN
    DECLARE dept_name VARCHAR(50);
    SELECT d.name INTO dept_name
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    WHERE e.employee_id = emp_id;
    RETURN dept_name;
END;
//

DELIMITER ;

-- Run functions
SELECT get_employee_department(1) AS department_name;
