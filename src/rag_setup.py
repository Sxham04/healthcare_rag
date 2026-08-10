#the main db setup script, splits the policies pdf into chunks and stores in the chroma db
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

#define directory paths
current_dir = os.path.dirname(os.path.abspath(__file__))
policies_dir = os.path.join(current_dir, "..", "data", "policies")
chroma_db_dir = os.path.join(current_dir, "..", "data", "chroma_db")

#clean existing vector database directory if present
if os.path.exists(chroma_db_dir):
    shutil.rmtree(chroma_db_dir)

#load pdf documents from policies folder
print("Loading PDF documents from data/policies...")
loader = PyPDFDirectoryLoader(policies_dir)
raw_documents = loader.load()

#split pdf text into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(raw_documents)
print(f"Total document chunks created: {len(docs)}")

#load local embeddings model
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#build and persist vector database
print("Building ChromaDB vector index...")
vector_db = Chroma.from_documents(
    documents=docs,
    embedding=embedding_function,
    persist_directory=chroma_db_dir
)

print("Vector database successfully built from PDF policy documents!")