# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 14:30:42 2024

@author: 13169
"""

# pip install pyodbc
# pip install pymssql

import requests
import pandas as pd
import io
import pyodbc
import sqlalchemy
import pymssql
from sqlalchemy import create_engine

import logging



url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/New%20York%20City/2024-09-10/2024-09-20?unitGroup=metric&include=days&key=CZV6ELVZB69ZXLTZWAZCZQ3CC&contentType=csv'
response = requests.get(url).text
print(response)
# with open('file55.csv', 'w') as f:
    # f.write(response)

    
df = pd.read_csv(io.StringIO(response))[['name','tempmax', 'tempmin', 'temp']]
df
# df.head(4)


########################

# Write the DataFrame to SQL Server as a new table

# Define the connection string
server = 'DESKTOP-NAIQFQH\SQLEXPRESS'  # Replace with your server name or IP address
database = 'NYC_Weather'  # Replace with your database name
driver = 'ODBC Driver 17 for SQL Server'  # Replace with the correct ODBC driver version

# Create connection string using SQLAlchemy and pyodbc
connection_string = f'mssql+pyodbc://@{server}/{database}?driver={driver}&trusted_connection=yes'

# Create SQLAlchemy engine
engine = create_engine(connection_string)

# Write the DataFrame to SQL Server as a new table
df.to_sql('Weather_33_Columns', engine, if_exists='replace', index=False)


########################

# Call the stored procedure called "TransferData" from Python. It reads the staging table,
# does some basic ETL, then writes the rows in the production table

# Using pyodbc. Why does not pymssql work here for stored procedure?

# Define the connection string for Windows Authentication
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-NAIQFQH\SQLEXPRESS;"  # Replace with your server or instance name
    "DATABASE=NYC_Weather;"
    "Trusted_Connection=yes;"  # Use Windows Authentication
)

# Create a connection
connection = pyodbc.connect(connection_string)

# Create a cursor and execute a query or stored procedure
cursor = connection.cursor()
cursor.execute("TransferData")

# Fetch results if applicable...the sp reads, then writes.
# for row in cursor:
#    print(row)

# Close the connection
cursor.close()
connection.close()


#########################
# Next steps:
# 1. Git Inititate (already done) and then link to Github (done). Then, add yidaveding as collaborator
# 2. Call the SQL stored procedure from Python   
# 3. Incorporate Python logging module
# 4. Refactor the stored procedure's INSERT INTO to something more appropriate (to address duplication potential)
# 5. Use Task Scheduler and then orchetrate from Python
