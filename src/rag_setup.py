#read policy files and create vector database
import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

current_dir = os.path.dirname(os.path.abspath(__file__))
policy_folder = os.path.join(current_dir, "..", "data", "policies")
db_folder = os.path.join(current_dir, "..", "data", "chroma_db")

#list policy files
files = ["visitor_policy.md", "admission_policy.md", "billing_policy.md"]

#load text documents
documents = []
for file_name in files:
    path = os.path.join(policy_folder, file_name)
    file = open(path, "r", encoding="utf-8")
    content = file.read()
    file.close()
    
    doc = Document(page_content=content, metadata={"source": file_name})
    documents.append(doc)

#split text into smaller chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
text_chunks = splitter.split_documents(documents)

#create free local embeddings model
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#save chunks to vector database
vector_db = Chroma.from_documents(
    documents=text_chunks,
    embedding=embedding_function,
    persist_directory=db_folder
)

print("Vector database setup complete. Policy chunks saved to ChromaDB.")