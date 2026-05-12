from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# =========================================
# Absolute path to faq.txt
# =========================================

BASE_DIR = Path(__file__).resolve().parent.parent

faq_path = BASE_DIR / "data" / "faq.txt"

# =========================================
# Load FAQ Document
# =========================================

loader = TextLoader(str(faq_path))

documents = loader.load()

# =========================================
# Split Documents
# =========================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = text_splitter.split_documents(documents)

# =========================================
# Embedding Model
# =========================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =========================================
# Store in ChromaDB
# =========================================

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    persist_directory=str(BASE_DIR / "vectorstore")
)

print("FAQ documents stored successfully!")