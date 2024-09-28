# importing libraries and dependencies
import numpy as np 
import pandas as pd 
import psycopg2 
from dash import Dash, html, dcc
import plotly.express as px
import os 
os.chdir('/home/ckapsalis/Desktop/mrkt_code_projects/vanderbilt/enhanced_indeed_raw/')


# connecting to a local PostgreSQL database & initializing the db's tables 
db_connector = psycopg2.connect(
    dbname='main',
    user='ckapsalis',
    password='ckapsalis',
    host='localhost',
    port='5432'
    )
cursor = db_connector.cursor()



# creating & populating the '_Companies' table
cursor.execute('''
SELECT * FROM _Companies
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS _Companies (
    company_x_id INT8 PRIMARY KEY,
    company VARCHAR(255) NOT NULL,
    company_rating NUMERIC(2,1),
    industry_cluster_1 VARCHAR(255),
    industry_cluster_2 VARCHAR(255),
    company_review_count INT8
)
''')

for col in companies.select_dtypes(include=['float64', 'int64']).columns:
    if col != 'company_x_id':  # Exclude the primary key - we should be getting errors upon trying to insert entries with missing primary keys
        companies[col] = companies[col].where(pd.notnull(companies[col]), None)
# Insert data into _Companies table
for index, row in companies.iterrows():
    try:
        values = (
            int(row['company_x_id']),  
            row['company'],  
            float(row['company_rating']) if pd.notnull(row['company_rating']) else None,  
            row['industry_cluster_1'],  
            row['industry_cluster_2'],  
            int(row['company_review_count']) if pd.notnull(row['company_review_count']) else None  
        )
        
        # Attempt to insert
        cursor.execute('''
        INSERT INTO _Companies (company_x_id, company, company_rating, industry_cluster_1, industry_cluster_2, company_review_count) 
        VALUES (%s, %s, %s, %s, %s, %s);
        ''', values)
    
    except Exception as e:
        # Log the error and problematic row index
        print(f"Error inserting row {index}: {row.to_dict()} - {e}")
        db_connector.rollback()  # Rollback on error
    else:
        db_connector.commit()  # Commit after every successful insert






# # creating & populating the '_Job_attributes' table
# cursor.execute('''
# DROP TABLE IF EXISTS _Job_attributes
# ''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS _Job_attributes (
    job_x_id INT8 PRIMARY KEY,
    display_title VARCHAR(255) NOT NULL,
    job_description VARCHAR(8000),
    job_type VARCHAR(255),
    snippet VARCHAR(8000),
    sponsored BOOL,
    shift_type VARCHAR(255),
    extracted_salary_min FLOAT8,
    extracted_salary_type VARCHAR(255),
    salary_snippet_currency VARCHAR(255),
    company_x_id INT8 NOT NULL,
    job_location VARCHAR(255) NOT NULL,
    min_hour_salary FLOAT8
)
''')

for col in job_attributes.select_dtypes(include=['float64', 'int64']).columns:
    if col != 'job_x_id':  # Exclude the primary key - we should be getting errors upon trying to insert entries with missing primary keys
        job_attributes[col] = job_attributes[col].where(pd.notnull(job_attributes[col]), None)
# Insert data into _Companies table
for _, row in job_attributes.iterrows():
    try:
        values = (
            row['job_x_id'] if pd.notnull(row['job_x_id']) else None,
            row['display_title'],  # String
            row['job_description'][:8000],  # String
            row['job_type'],  # String
            row['snippet'][:8000],  # String
            bool(row['sponsored']) if pd.notnull(row['sponsored']) else None,  # Handle NaN for boolean
            row['shift_type'],  # String
            float(row['extracted salary/min']) if pd.notnull(row['extracted salary/min']) else None,  # Handle NaN
            row['extracted salary/type'],  # String
            row['salary snippet/currency'],  # String
            int(row['company_x_id']),  # INT8 (should not be NaN if properly filled - raise error otherwise)
            row['job_location'],  # String
            float(row['min_hourly_salary']) if pd.notnull(row['min_hourly_salary']) else None  # Handle NaN

            )
        cursor.execute('''
        INSERT INTO _Job_attributes (job_x_id, display_title, job_description, job_type, snippet, sponsored, 
                                      shift_type, extracted_salary_min, extracted_salary_type, 
                                      salary_snippet_currency, company_x_id, job_location, 
                                      min_hour_salary) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        ''', values)
    except Exception as e:
        print(f"Error inserting row: {row} - {e}")
        db_connector.rollback()  # Rollback on error
    else:
        db_connector.commit()  # Commit after every successful insert
        
        
        
        
        
        
# # Creating & populating the _Job_requirements table 
# cursor.execute('''
# DROP TABLE IF EXISTS _Job_requirements
# ''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS _Job_requirements (
    job_x_id INT8,
    job_requirement_name VARCHAR(255)
)

''')

for _, row in job_requirements.iterrows():
    try:
        values = (
            row['job_x_id'],  # i want it to crash if a null job_x_id is given
            row['job_requirement_name']  # String
            )
        cursor.execute('''
        INSERT INTO _Job_requirements (job_x_id, job_requirement_name) 
        VALUES (%s, %s);
        ''', values)
    except Exception as e:
        print(f"Error inserting row: {row} - {e}")
        db_connector.rollback()  # Rollback on error
    else:
        db_connector.commit()  # Commit after every successful insert





# creating & populating the _Job_benefits table 
cursor.execute('''
DROP TABLE IF EXISTS _Job_benefits
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS _Job_benefits (
    job_x_id INT8,
    job_benefit_value VARCHAR(255)

)

''')

for _, row in job_benefits.iterrows():
    try:
        values = (
            row['job_x_id'],  # i want it to crash if a null job_x_id is given
            row['job_benefit_value']  # String
            )
        cursor.execute('''
        INSERT INTO _Job_benefits (job_x_id, job_benefit_value) 
        VALUES (%s, %s);
        ''', values)
    except Exception as e:
        print(f"Error inserting row: {row} - {e}")
        db_connector.rollback()  # Rollback on error
    else:
        db_connector.commit()  # Commit after every successful insert

db_connector.commit()




# Close the connection
cursor.close()
db_connector.close()





