# Your code goes here!
import csv
import psycopg2
import os

import ipdb
from decimal import Decimal

def table_creation_query():
    return "CREATE TABLE employees (first_name varchar(255) NOT NULL, last_name varchar(255) NOT NULL, job_title varchar(255) NOT NULL, full_or_part_time char(1) NOT NULL, department varchar(255) NOT NULL, annual_salary money NOT NULL);"

def clean_data(csv_row):
    cleaned = {}
    full_name = csv_row['Name'].split(',  ')
    cleaned['first_name'] = full_name[1]
    cleaned['last_name'] = full_name[0]
    cleaned['job_title'] = csv_row['Job Titles']
    cleaned['full_or_part_time'] = csv_row['Full or Part-Time']
    cleaned['department'] = csv_row['Department']
    salary_or_hourly = csv_row['Salary or Hourly']
    if salary_or_hourly == 'Salary':
        annual_salary = Decimal(csv_row['Annual Salary'])
    else:
        annual_salary = int(csv_row['Typical Hours']) * Decimal(csv_row['Hourly Rate']) * 50
    cleaned['annual_salary'] = annual_salary
    return cleaned

connection = psycopg2.connect(f"dbname=chicago_salaries user={os.getlogin()}")

with connection.cursor() as cursor:
    cursor.execute(table_creation_query())

    dir_path = os.getcwd()
    csv_path = os.path.join(dir_path, "Current_Employee_Names__Salaries__and_Position_Titles.csv")
    with open(csv_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            cleaned_data = clean_data(row)
            cursor.execute("INSERT INTO employees (first_name, last_name, job_title, full_or_part_time, department, annual_salary) VALUES (%s, %s, %s, %s, %s, %s);", (cleaned_data['first_name'], cleaned_data['last_name'], cleaned_data['job_title'], cleaned_data['full_or_part_time'], cleaned_data['department'], cleaned_data['annual_salary'],))

connection.commit()
cursor.close()
connection.close()