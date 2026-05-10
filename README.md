# 🦜🔗 LangChain Bangla

A comprehensive LangChain tutorial series in Bangla — covering prompt engineering, LLM integration, memory, LCEL, output parsers, document loaders, embeddings, and vector stores.

---

## 📚 Module 1 — Core LangChain Concepts

| #   | Notebook                                                                                    | Topics Covered                                      |
| --- | ------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| 00  | [Introduction](Module_1/00_introduction.ipynb)                                              | Overview of LangChain, setup & environment          |
| 01  | [Python Basics for LangChain](Module_1/02_python_basics_for_langchain.ipynb)                | Python concepts needed for LangChain development    |
| 02  | [Prompt Engineering](Module_1/003_prompt_engineering.ipynb)                                 | Prompt templates, few-shot prompting, prompt design |
| 03  | [Initial LLM Call via LangChain](Module_1/004_initial_llm_call_via_lanchain.ipynb)          | Connecting to LLMs, making your first API call      |
| 04  | [LangChain with Basic History](Module_1/005_lanchain_with_basic_history.ipynb)              | Maintaining conversation context                    |
| 05  | [LCEL — LangChain Expression Language](Module_1/006_LCEL.ipynb)                             | Building chains using the `\|` pipe syntax          |
| 06  | [Output Parser](Module_1/007_OutputParser.ipynb)                                            | Parsing LLM responses into structured data          |
| 07  | [Memory & History](Module_1/008_memory_history.ipynb)                                       | ConversationBufferMemory, chat history management   |
| 08  | [Document Loader & Text Splitter](Module_1/009_document_loader_and_text_splitter.ipynb)     | Loading docs, chunking strategies                   |
| 09  | [Embeddings, Vectors & Vector Store](Module_1/010_embeddings_vector_and_vector_store.ipynb) | Semantic search, FAISS/Chroma, RAG foundations      |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- An OpenAI (or compatible) API key

### Installation

```bash
git clone https://github.com/your-username/langchain-bangla.git
cd langchain-bangla

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

### Run Notebooks

```bash
jupyter notebook
```

Then navigate to `Module_1/` and open any notebook.

---

## 📁 Project Structure

```
langchain-bangla/
├── Module_1/               # Core LangChain notebooks
│   ├── 00_introduction.ipynb
│   ├── 02_python_basics_for_langchain.ipynb
│   ├── 003_prompt_engineering.ipynb
│   ├── 004_initial_llm_call_via_lanchain.ipynb
│   ├── 005_lanchain_with_basic_history.ipynb
│   ├── 006_LCEL.ipynb
│   ├── 007_OutputParser.ipynb
│   ├── 008_memory_history.ipynb
│   ├── 009_document_loader_and_text_splitter.ipynb
│   └── 010_embeddings_vector_and_vector_store.ipynb
├── Data/                   # Sample datasets
├── Projects/               # Hands-on projects
├── requirements.txt
└── .env
```

---

## 🛠️ Tech Stack

- [LangChain](https://www.langchain.com/)
- [OpenAI API](https://platform.openai.com/)
- [FAISS](https://faiss.ai/) / [Chroma](https://www.trychroma.com/)
- [Jupyter Notebook](https://jupyter.org/)

---

## 📄 License

This project is open-source. See [LICENCE](LICENCE) for details.
