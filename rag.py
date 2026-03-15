import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.tools import tool

# ── Embeddings Model ────────────────────────────────────
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ── Vector Store ────────────────────────────────────────
CHROMA_DIR = "./chroma_db"
vectorstore = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings
)

# ── Text Splitter ───────────────────────────────────────
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)


def load_file(file_name: str, folder_path: str):
    """Load a file and return documents."""
    full_path = os.path.join(folder_path, file_name)

    if not os.path.exists(full_path):
        return None, f"Error: File '{file_name}' not found in '{folder_path}'"

    ext = os.path.splitext(file_name)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(full_path)
    elif ext == ".docx":
        loader = Docx2txtLoader(full_path)
    elif ext == ".txt":
        loader = TextLoader(full_path, encoding="utf-8")
    else:
        return None, f"Unsupported file type '{ext}'"

    docs = loader.load()
    return docs, None


@tool
def read_and_index_file(file_name: str, folder_path: str) -> str:
    """
    Read a file (PDF, DOCX, TXT), index it for smart search, and return a summary preview.
    Use this when the user asks to read, open, or summarize a file.

    Args:
        file_name: The name of the file (e.g. 'report.pdf')
        folder_path: The folder where the file is (e.g. 'C:/Users/elkat/Downloads')

    Returns:
        First 1000 characters of the file as preview.
    """
    docs, error = load_file(file_name, folder_path)
    if error:
        return error

    # Split and index
    chunks = splitter.split_documents(docs)
    vectorstore.add_documents(chunks)

    preview = docs[0].page_content[:1000]
    return f"File '{file_name}' indexed successfully ({len(chunks)} chunks).\n\nPreview:\n{preview}"


@tool
def search_in_file(query: str) -> str:
    """
    Search for specific information inside previously read files.
    Use this when the user asks follow up questions about a file that was already read.

    Args:
        query: What to search for inside the file.

    Returns:
        Most relevant chunks from the file.
    """
    results = vectorstore.similarity_search(query, k=3)

    if not results:
        return "No relevant information found. Please read a file first."

    output = ""
    for i, doc in enumerate(results, 1):
        output += f"\n[Chunk {i}]:\n{doc.page_content}\n"

    return output