#load patient csv data into sqlite database
import sqlite3
import pandas as pd

csv_file = "../data/healthcare_dataset.csv"
db_file = "../data/healthcare.db"

data = pd.read_csv(csv_file)

#clean column names
clean_columns = []
for column in data.columns:
    new_name = column.strip().lower().replace(" ", "_")
    clean_columns.append(new_name)

data.columns = clean_columns

#format date and billing columns
data["date_of_admission"] = pd.to_datetime(data["date_of_admission"])
data["discharge_date"] = pd.to_datetime(data["discharge_date"])
data["billing_amount"] = data["billing_amount"].round(2)

connection = sqlite3.connect(db_file)

#write data to patients table
data.to_sql("patients", connection, if_exists="replace", index=False)

connection.close()

print("Database setup complete. Clean patient data saved to SQLite database.")