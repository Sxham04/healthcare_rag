#script loads ChromaDB vector database, retrieves policy text relevant to a user question, and uses llama3.2 via ChatOllama to answer policy queries.

#query hospital policies using local rag pipeline
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

#define vector database path using script location
current_dir = os.path.dirname(os.path.abspath(__file__))
db_folder = os.path.join(current_dir, "..", "data", "chroma_db")

embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_db = Chroma(
    persist_directory=db_folder,
    embedding_function=embedding_function
)

#create local llama model
llm = ChatOllama(model="llama3.2", temperature=0)

#define rag prompt template
rag_prompt = ChatPromptTemplate.from_template("""
You are a helpful hospital administration assistant.
Answer the user question based ONLY on the following policy context:

Policy Context:
{context}

Question: {question}

Instruction: Keep your answer clear, accurate, and brief. If the policy context does not contain the answer, say "I cannot find this information in the hospital policies."
""")

#main query function
def ask_policy_data(question):
    #retrieve top 3 relevant chunks
    docs = vector_db.similarity_search(question, k=3)
    
    #combine retrieved chunk texts
    context_text = "\n\n".join([doc.page_content for doc in docs])
    
    #generate answer using llama
    chain = rag_prompt | llm
    response = chain.invoke({"context": context_text, "question": question})
    return response.content

#test run script directly
if __name__ == "__main__":
    test_question = "What are the visiting hours for the hospital?"
    print(f"Question: {test_question}")
    answer = ask_policy_data(test_question)
    print(f"Answer:\n{answer}")