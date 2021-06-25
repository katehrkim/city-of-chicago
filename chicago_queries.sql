-- Write your Queries here
-- 1. Find the employee being paid the most
SELECT first_name, last_name, annual_salary
FROM employees
ORDER BY annual_salary DESC
LIMIT 1;

-- 2. Find the employee being paid the least

SELECT first_name, last_name, annual_salary
FROM employees
ORDER BY annual_salary ASC
LIMIT 1;

-- 3. Find the department with the highest average salary

SELECT department, AVG(CAST(annual_salary AS DECIMAL))
FROM employees
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1;

-- 4. Find the department with the lowest average salary

SELECT department, AVG(CAST(annual_salary AS DECIMAL))
FROM employees
GROUP BY 1
ORDER BY 2 ASC
LIMIT 1;

-- 5. Find the average salary difference between full time and part time workers

SELECT AVG(CAST(annual_salary AS DECIMAL)) - 
(SELECT AVG(CAST(annual_salary AS DECIMAL))
FROM employees
WHERE full_or_part_time = 'P')
AS salary_difference
FROM employees
WHERE full_or_part_time = 'F';

-- 6. Find the most common first name

SELECT first_name, COUNT(first_name) AS occurrences
FROM employees
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1;

-- 7. Find the most common last name

SELECT last_name, COUNT(first_name) AS occurrences
FROM employees
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1;

-- 8. If there are people with the same name, find what their job titles, departments, and annual salaries are

SELECT *
FROM employees emp1
WHERE exists(
  SELECT *
  FROM employees emp2
  WHERE emp1.first_name = emp2.first_name
  AND emp1.last_name = emp2.last_name
  AND emp1.annual_salary <> emp2.annual_salary
)
ORDER BY first_name, last_name;
