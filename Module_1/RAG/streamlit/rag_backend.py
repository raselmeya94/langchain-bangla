"""
rag_backend.py  —  RAG pipeline for multi-document chatbot
Dependencies:
    pip install langchain langchain-community langchain-huggingface
                faiss-cpu pypdf sentence-transformers groq langchain-groq
"""

import os
import tempfile
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import  RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate


# ─────────────────────────────────────────────
# 1. DOCUMENT LOADER
# ─────────────────────────────────────────────

def documents_loader(pdf_paths: list[str]) -> list:
    """
    Load one or multiple PDF files and return a flat list of LangChain Documents.

    Args:
        pdf_paths: list of absolute file paths to PDF files.

    Returns:
        List of Document objects with page_content and metadata.
    """
    all_docs = []
    for path in pdf_paths:
        loader = PyPDFLoader(path)
        docs = loader.load()
        # Attach the original filename to every page for provenance
        for doc in docs:
            doc.metadata["source_file"] = Path(path).name
        all_docs.extend(docs)
    return all_docs


# ─────────────────────────────────────────────
# 2. TEXT SPLITTER
# ─────────────────────────────────────────────

def splitter(documents: list, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    """
    Split documents into overlapping chunks for better retrieval.

    Args:
        documents:    List of LangChain Document objects.
        chunk_size:   Maximum characters per chunk.
        chunk_overlap: Overlap between consecutive chunks.

    Returns:
        List of smaller Document chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = text_splitter.split_documents(documents)
    return chunks


# ─────────────────────────────────────────────
# 3. EMBEDDINGS MODEL
# ─────────────────────────────────────────────

def get_embeddings(model_name: str = "BAAI/bge-small-en-v1.5"):
    """
    Return a HuggingFace sentence-transformer embedding model.
    BGE-small is fast and high-quality for retrieval tasks.

    Args:
        model_name: HuggingFace model identifier.

    Returns:
        HuggingFaceEmbeddings instance.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    return embeddings


# ─────────────────────────────────────────────
# 4. VECTOR STORE
# ─────────────────────────────────────────────

def vector_store(chunks: list, embeddings, persist_path: str = "faiss_index"):
    """
    Build (or update) a FAISS vector store from document chunks.

    Args:
        chunks:       List of Document chunks.
        embeddings:   Embedding model instance.
        persist_path: Directory to save the FAISS index for reuse.

    Returns:
        FAISS vector store (retriever-ready).
    """
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(persist_path)
    return db


def load_vector_store(embeddings, persist_path: str = "faiss_index"):
    """Load an existing FAISS index from disk."""
    return FAISS.load_local(persist_path, embeddings, allow_dangerous_deserialization=True)


# ─────────────────────────────────────────────
# 5. LLM MODEL
# ─────────────────────────────────────────────

def llm_model(api_key: str, model_name: str = "llama-3.3-70b-versatile", temperature: float = 0.3):
    """
    Initialise a Groq-hosted LLM (fast, free tier available).
    Swap model_name for any Groq-supported model, e.g.:
      - "llama-3.3-70b-versatile"   (default)
      - "mixtral-8x7b-32768"
      - "gemma2-9b-it"

    Args:
        api_key:     Groq API key.
        model_name:  Groq model identifier.
        temperature: Sampling temperature (0 = deterministic).

    Returns:
        ChatGroq LLM instance.
    """
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name=model_name,
        temperature=temperature,
        max_tokens=2048,
    )
    return llm


# ─────────────────────────────────────────────
# 6. PROCESS DOCUMENTS  (orchestrator)
# ─────────────────────────────────────────────

def process_documents(
    pdf_paths: list[str],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    persist_path: str = "faiss_index",
):
    """
    Full pipeline: load → split → embed → store.

    Args:
        pdf_paths:    Paths to uploaded PDF files.
        chunk_size:   Chunk size for splitter.
        chunk_overlap: Overlap for splitter.
        persist_path: Where to persist the FAISS index.

    Returns:
        Tuple of (FAISS vector store, embeddings model, chunk count).
    """
    docs = documents_loader(pdf_paths)
    chunks = splitter(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    embeddings = get_embeddings()
    db = vector_store(chunks, embeddings, persist_path=persist_path)
    return db, embeddings, len(chunks)


# ─────────────────────────────────────────────
# 7. CONVERSATIONAL QA CHAIN
# ─────────────────────────────────────────────

CUSTOM_PROMPT = PromptTemplate(
    input_variables=["context", "question", "chat_history"],
    template="""You are an expert document analyst. Use ONLY the provided context to answer.
If the answer isn't in the context, say "I don't find that in the uploaded documents."
Be concise, accurate, and cite the source file when possible.

Chat History:
{chat_history}

Context from documents:
{context}

Question: {question}

Answer:""",
)


def build_qa_chain(db, llm, k: int = 4):
    """
    Build a ConversationalRetrievalChain with memory.

    Args:
        db:  FAISS vector store.
        llm: Language model instance.
        k:   Number of top chunks to retrieve per query.

    Returns:
        ConversationalRetrievalChain ready for .invoke()
    """
    retriever = db.as_retriever(
        search_type="mmr",          # Maximal Marginal Relevance for diversity
        search_kwargs={"k": k, "fetch_k": k * 3},
    )

    memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
        k=6,                        # Remember last 6 exchanges
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": CUSTOM_PROMPT},
        verbose=False,
    )
    return chain


# ─────────────────────────────────────────────
# 8. ASK A QUESTION
# ─────────────────────────────────────────────

def ask_question(chain, question: str) -> dict:
    """
    Send a question through the QA chain and return a structured response.

    Args:
        chain:    ConversationalRetrievalChain instance.
        question: User's question string.

    Returns:
        Dict with keys:
          - "answer":  The model's answer string.
          - "sources": List of dicts {file, page, snippet}.
    """
    result = chain.invoke({"question": question})
    answer = result.get("answer", "").strip()

    # Build deduplicated source list
    sources = []
    seen = set()
    for doc in result.get("source_documents", []):
        meta = doc.metadata
        key = (meta.get("source_file", "unknown"), meta.get("page", "?"))
        if key not in seen:
            seen.add(key)
            sources.append(
                {
                    "file": meta.get("source_file", "unknown"),
                    "page": meta.get("page", "?"),
                    "snippet": doc.page_content[:200].replace("\n", " "),
                }
            )

    return {"answer": answer, "sources": sources}


# ─────────────────────────────────────────────
# 9. SAVE UPLOADED FILES TO TEMP DIR
# ─────────────────────────────────────────────

def save_uploaded_files(uploaded_files) -> list[str]:
    """
    Persist Streamlit UploadedFile objects to a temp directory.

    Args:
        uploaded_files: List of Streamlit UploadedFile objects.

    Returns:
        List of absolute file paths on disk.
    """
    tmp_dir = tempfile.mkdtemp(prefix="rag_uploads_")
    paths = []
    for uf in uploaded_files:
        dest = os.path.join(tmp_dir, uf.name)
        with open(dest, "wb") as f:
            f.write(uf.getbuffer())
        paths.append(dest)
    return paths