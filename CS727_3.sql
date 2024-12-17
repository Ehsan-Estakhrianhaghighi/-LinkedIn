USE company_db;

--Rank Employees by Salary
SELECT e.first_name, e.last_name, s.amount,
       RANK() OVER (ORDER BY s.amount DESC) AS salary_rank
FROM employees e
JOIN salaries s ON e.employee_id = s.employee_id;

--Dense Rank Employees by Salary
SELECT e.first_name, e.last_name, s.amount,
       DENSE_RANK() OVER (ORDER BY s.amount DESC) AS salary_dense_rank
FROM employees e
JOIN salaries s ON e.employee_id = s.employee_id;


--Lead Function Example
SELECT e.first_name, e.last_name, s.amount,
       LEAD(s.amount, 1) OVER (ORDER BY s.amount DESC) AS next_salary
FROM employees e
JOIN salaries s ON e.employee_id = s.employee_id;


--Lag Function Example
SELECT e.first_name, e.last_name, s.amount,
       LAG(s.amount, 1) OVER (ORDER BY s.amount DESC) AS previous_salary
FROM employees e
JOIN salaries s ON e.employee_id = s.employee_id;


-- Ntile Function Example
SELECT e.first_name, e.last_name, s.amount,
       NTILE(4) OVER (ORDER BY s.amount DESC) AS quartile
FROM employees e
JOIN salaries s ON e.employee_id = s.employee_id;


--Percent Rank Function Example
SELECT 
    e.first_name, 
    e.last_name, 
    s.amount,
    PERCENT_RANK() OVER (ORDER BY s.amount DESC) AS 'percent_rank'
FROM employees e
JOIN salaries s ON e.employee_id = s.employee_id;



--Cume Dist Function Example
SELECT e.first_name, e.last_name, s.amount,
       CUME_DIST() OVER (ORDER BY s.amount DESC) AS 'cume_dist'
FROM employees e
JOIN salaries s ON e.employee_id = s.employee_id;

-- 3-Month Moving Average of Salaries
SELECT e.first_name, e.last_name, s.amount,
       AVG(s.amount) OVER (ORDER BY s.start_date 
                           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg
FROM employees e
JOIN salaries s ON e.employee_id = s.employee_id;


--Running Total Salary by Department
SELECT d.name AS department, e.first_name, e.last_name, s.amount,
       SUM(s.amount) OVER (PARTITION BY d.name ORDER BY s.amount ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM departments d
JOIN employees e ON d.department_id = e.department_id
JOIN salaries s ON e.employee_id = s.employee_id;

--Running Total Salary by Department Using Range
SELECT d.name AS department, e.first_name, e.last_name, s.amount,
       SUM(s.amount) OVER (PARTITION BY d.name ORDER BY s.amount RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM departments d
JOIN employees e ON d.department_id = e.department_id
JOIN salaries s ON e.employee_id = s.employee_id;

--Total Salary Expenditure by Department with ROLLUP
SELECT d.name AS department, SUM(s.amount) AS total_expenditure
FROM departments d
JOIN employees e ON d.department_id = e.department_id
JOIN salaries s ON e.employee_id = s.employee_id
GROUP BY ROLLUP(d.name);


--Total Salary Expenditure by Department with CUBE, unfortunately Mysql does not support secondary search engine
SELECT d.name AS department ,d.location,SUM(s.amount) AS total_expenditure
FROM departments d
JOIN employees e ON d.department_id = e.department_id
JOIN salaries s ON e.employee_id = s.employee_id
GROUP BY CUBE(d.name,d.location);

-- Total Salary Expenditure by Department with ROLLUP
-- SELECT d.name AS department, SUM(s.amount) AS total_expenditure
-- FROM departments d
-- JOIN employees e ON d.department_id = e.department_id
-- JOIN salaries s ON e.employee_id = s.employee_id
-- GROUP BY ROLLUP(d.name);

-- Concatenate Employee Names for Each Department
SELECT d.name AS department,
       GROUP_CONCAT(CONCAT(e.first_name, ' ', e.last_name) ORDER BY e.last_name SEPARATOR ', ') AS employee_names
FROM departments d
JOIN employees e ON d.department_id = e.department_id
GROUP BY d.name;


--Number of Employees by Department with GROUPING SETs, unfortunately Grouping set is not supported in MYSQL.
SELECT d.name AS department, COUNT(e.employee_id) AS num_employees,
       GROUPING(d.name) AS is_total
FROM departments d
JOIN employees e ON d.department_id = e.department_id
GROUP BY GROUPING SETS ((d.name), ());

--Employees by Department and location with ROLLUP
SELECT d.name AS department_name, d.location, COUNT(e.employee_id) AS num_employees
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY ROLLUP(d.name, d.location);


-- Handle NULL Salaries by Providing a Default Value
SELECT e.first_name, e.last_name,
       IFNULL(s.amount, 0) AS salary
FROM employees e
LEFT JOIN salaries s ON e.employee_id = s.employee_id;


-- Find minimum and maximum salary in each department
SELECT d.name AS department,
       MIN(s.amount) AS min_salary,
       MAX(s.amount) AS max_salary
FROM departments d
JOIN employees e ON d.department_id = e.department_id
JOIN salaries s ON e.employee_id = s.employee_id
GROUP BY d.name;


