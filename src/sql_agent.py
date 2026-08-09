#query patient database using local llama model
import os
import sqlite3
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "..", "data", "healthcare.db")

#create local llama model
llm = ChatOllama(model="llama3.2", temperature=0)

#define sql generation prompt
sql_prompt = ChatPromptTemplate.from_template("""
You are an expert SQLite database engineer.

Database Table Name: patients
Table Columns: name, age, gender, blood_type, medical_condition, date_of_admission, doctor, hospital, insurance_provider, billing_amount, room_number, admission_type, discharge_date, medication, test_results

User Question: {question}

Instructions:
1. Return ONLY the raw SQL query.
2. Do not include markdown code blocks (no ```sql).
3. Do not add any text explanations.
""")

#function to run query on sqlite
def run_sql_query(query):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results

#main question function
def ask_patient_data(question):
    #generate sql query
    chain = sql_prompt | llm
    sql_response = chain.invoke({"question": question})
    clean_sql = sql_response.content.strip().replace("```sql", "").replace("```", "")
    print(f"Generated SQL: {clean_sql}")
    
    #execute sql query
    try:
        data = run_sql_query(clean_sql)
        return f"Database Query Results: {data}"
    except Exception as e:
        return f"Error executing query: {str(e)}"

#test run script directly
if __name__ == "__main__":
    test_question = "How many patients are in the database?"
    print(f"Question: {test_question}")
    answer = ask_patient_data(test_question)
    print(f"Answer: {answer}")