use olapdb;

CREATE TABLE Employee (
    row_num INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(25) NOT NULL,
    lastname VARCHAR(25) NOT NULL,
    department VARCHAR(25),
    salary DOUBLE
);

INSERT INTO Employee (firstname, lastname, department, salary) VALUES
('John', 'Doe', 'HR', 50000.00),
('Jane', 'Smith', 'IT', 60000.00),
('Emily', 'Jones', 'Finance', 55000.00),
('Michael', 'Brown', 'IT', 62000.00),
('Jessica', 'Taylor', 'HR', 52000.00),
('Daniel', 'Williams', 'Finance', 58000.00),
('Laura', 'Wilson', 'Marketing', 53000.00),
('Chris', 'Davis', 'IT', 61000.00),
('Anna', 'Garcia', 'Marketing', 54000.00),
('David', 'Martinez', 'Finance', 56000.00),
('Sarah', 'Robinson', 'HR', 51000.00),
('James', 'Clark', 'IT', 63000.00);

SELECT row_num, firstname, lastname, salary, department, 
RANK() OVER(PARTITION BY department ORDER BY salary) as s_rank,
DENSE_RANK() OVER(PARTITION BY department ORDER BY salary) as s_dense_rank
FROM employee;


SELECT row_num, firstname, lastname, salary,  
RANK() OVER (ORDER BY salary) as s_rank,
ROUND(PERCENT_RANK() OVER(ORDER BY salary),2) as s_per_rank,
ROUND(PERCENT_RANK() OVER(ORDER BY salary),2)*100 as "s_per_rank%"
FROM employee;

SELECT row_num, firstname, lastname, salary,  
RANK() OVER (ORDER BY salary) as s_rank,
ROUND(CUME_DIST() OVER(ORDER BY salary),2) as s_cum_dist,
ROUND(CUME_DIST() OVER(ORDER BY salary),2)*100 as "s_cum_dist%"
FROM employee;

SELECT ROW_NUMBER() OVER (ORDER BY salary),
RANK() OVER( ORDER BY salary), salary
FROM employee;


SELECT row_num, firstname, salary,
NTILE(5) OVER(ORDER BY salary)
FROM employee;

CREATE table salesproduct(
    saledate varchar(50),
    product varchar(50),
    value INT
);

INSERT INTO salesproduct (saledate, product, value) VALUES
('2024-06-01', 'Laptop', 1200),
('2024-06-02', 'Smartphone', 800),
('2024-06-03', 'Tablet', 600),
('2024-06-04', 'Monitor', 300),
('2024-06-05', 'Keyboard', 100),
('2024-06-06', 'Mouse', 50),
('2024-06-07', 'Printer', 150),
('2024-06-08', 'Camera', 900),
('2024-06-09', 'Headphones', 200),
('2024-06-10', 'Speakers', 250);

SELECT saledate, product, value, AVG(value)
OVER(ORDER BY saledate ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) as "3-day-avg"
FROM salesproduct;

SELECT saledate, product, value, AVG(value)
OVER(ORDER BY saledate ROWS 1 PRECEDING) as "3-day-avg"
FROM salesproduct;

SELECT saledate, product, value, 
SUM(value) OVER(PARTITION BY product ORDER BY saledate ROWS UNBOUNDED PRECEDING) as "running total per product",
AVG(value) OVER(PARTITION BY product ORDER BY saledate ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) as "3-day-avg"
FROM salesproduct ;

SELECT saledate, product, value, 
SUM(value) OVER(PARTITION BY product ORDER BY saledate ROWS UNBOUNDED PRECEDING) as "running total per product",
ROUND(AVG(value) OVER(PARTITION BY product ORDER BY saledate ROWS UNBOUNDED PRECEDING),2) as "runnign total avg"
FROM salesproduct ;

CREATE table sales(
    product CHAR(1),
    quarters CHAR(2),
    region VARCHAR(20),
    salesqty INT
);

INSERT INTO sales (product, quarters, region, salesqty) VALUES
('A', 'Q1', 'North', 100),
('B', 'Q2', 'South', 150),
('A', 'Q2', 'North', 200),
('B', 'Q4', 'North', 250),
('A', 'Q1', 'South', 180),
('B', 'Q3', 'North', 220),
('A', 'Q3', 'South', 140),
('B', 'Q4', 'South', 160),
('A', 'Q1', 'North', 190),
('B', 'Q2', 'South', 210),
('A', 'Q3', 'North', 230),
('B', 'Q4', 'South', 170),
('A', 'Q1', 'South', 110),
('B', 'Q2', 'North', 130);


SELECT product, quarters, region, SUM(salesqty) AS totalsales
FROM sales
GROUP BY product, quarters, region
ORDER BY product, quarters, region;


SELECT region, count(quarters), sum(salesqty) AS totalsales
FROM sales
GROUP BY region with ROLLUP;

SELECT product, quarters,region, count(quarters), sum(salesqty) AS totalsales
FROM sales
GROUP BY product, quarters, region with ROLLUP;

SELECT product, quarters, region, SUM(salesqty) AS totalsales,
GROUPING (product) as prductflag,GROUPING(quarters) as quarterflag,
GROUPING (region) as regionflag
FROM sales
GROUP BY ROLLUP (product, quarters, region);

SELECT DATABASE();
