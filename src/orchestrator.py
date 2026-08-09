#inspect the incoming user question and routes them to the two categories
#ask_patient_data which fetches data from database
#ask_policy_data which fetches data using the RAG agent

import sys
import os

#add current directory to python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from sql_agent import ask_patient_data
from rag_agent import ask_policy_data
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

#create local llama model
llm = ChatOllama(model="llama3.2", temperature=0)

#define routing prompt
router_prompt = ChatPromptTemplate.from_template("""
You are a classification assistant for a hospital system.

Classify the user question into ONE of these two categories:
- "DATABASE": Questions about specific patients, counts, medical conditions, billing amounts, doctors, rooms, dates of admission, or database numbers.
- "POLICY": Questions about hospital rules, visitor hours, admission procedures, billing guidelines, or general hospital policies.

User Question: {question}

Instruction: Reply with ONLY "DATABASE" or "POLICY". Do not include extra text.
""")

def route_query(question):
    #classify question
    chain = router_prompt | llm
    classification = chain.invoke({"question": question}).content.strip().upper()
    print(f"Query Classification: {classification}")
    
    #route to corresponding agent
    if "DATABASE" in classification:
        return ask_patient_data(question)
    elif "POLICY" in classification:
        return ask_policy_data(question)
    else:
        #fallback to policy agent
        return ask_policy_data(question)

#test run script directly
if __name__ == "__main__":
    test_db_q = "How many patients are admitted with Diabetes?"
    print(f"Test 1: {test_db_q}")
    print(route_query(test_db_q))
    
    print("\n" + "="*40 + "\n")
    
    test_policy_q = "What is the policy for ICU visitors?"
    print(f"Test 2: {test_policy_q}")
    print(route_query(test_policy_q))