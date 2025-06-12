# 🧾 Invoice Reimbursement System

An AI-powered system to automate invoice reimbursement policy compliance for HR teams. Upload employee invoices and a policy document — the system determines reimbursement eligibility using an LLM, stores results in a vector database, and lets you chat with the system to query historical results.

---

## 📽️ Demo

A short walkthrough demo is stored in the [`media/`](media/) folder. You can upload this to YouTube, Streamlit Cloud, or GitHub releases as needed.

---

## 🚀 Tech Stack

| Component         | Technology                        |
|------------------|------------------------------------|
| Backend API      | FastAPI                            |
| Frontend UI      | Streamlit                          |
| LLMs             | Gemini 2.0 Flash (fallback: LLaMA3 via Groq) |
| Framework        | LangChain                          |
| Embeddings       | HuggingFace Sentence Transformers  |
| Vector DB        | ChromaDB                           |
| PDF Parsing      | PyMuPDF (fallback: pdfplumber)     |
| ZIP Handling     | zipfile (fallback: shutil)         |
| Config & Env     | YAML + dotenv                      |
| Logging          | Python Logging (RotatingFileHandler) |

---

## 📁 Folder Structure
```
invoice_reimbursement/
│
├── app.py # FastAPI app
├── main.py # CLI-based invoice processor (optional)
├── requirements.txt
├── setup.py
├── config.yaml
├── .env # API keys (NOT checked in)
├── README.md
│
├── data/
│ ├── raw_zips/ # Uploaded ZIP files
│ └── extracted_invoices/ # Unzipped PDF invoices
│
├── static/
│ ├── results.json # Latest processed results
│ └── styles/
│ └── style.css # Custom CSS for Streamlit
│
├── logs/
│ └── app.log # Logger output
│
├── utils/
│ ├── logger.py # Logging setup
│ ├── config.py # Loads YAML + .env
│ ├── exceptions.py # Custom exception classes
│ ├── zip_handler.py # ZIP extraction logic
│ ├── pdf_parser.py # PDF parsing w/ fallback
│ ├── embedding.py # Embedding model loader
│ ├── llm_utils.py # Gemini + Groq with fallback
│ ├── batch_processor.py # Multithreaded invoice processing
│
├── vector_db/
│ └── chromadb_utils.py # ChromaDB integration
│
├── prompt_lib/
│ ├── invoice_prompts.py # Prompt for invoice decision
│ └── chatbot_prompts.py # Prompt for query chatbot
│
├── streamlit_app/
│ └── app.py # Streamlit frontend
│
├── media/
│ └── demo.mp4 # Optional video demo
```

---

## 🧠 Features

### Part 1: Invoice Reimbursement Analyzer
- Upload HR policy + invoices ZIP
- Uses LLM to classify:
  - Fully Reimbursed
  - Partially Reimbursed
  - Declined
- Embeds text + metadata to ChromaDB
- Outputs structured JSON

### Part 2: Query Chatbot (RAG)
- Ask questions about invoices (e.g., by employee, date, status)
- Retrieves relevant results using vector similarity + metadata
- Responds in Markdown format

---

## ⚙️ Installation

```bash
# Clone repo & enter directory
git clone <your-repo-url>
cd invoice_reimbursement

# Create virtual env (optional)
conda create -n invoice_reimbursement python=3.10
conda activate invoice_reimbursement

# Install dependencies
pip install -r requirements.txt

```
---


## 🔑 Environment Setup

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
```

## 🧪 Running the App
Start the FastAPI backend:
uvicorn app:app --reload


Start the Streamlit frontend:
streamlit run streamlit_app/app.py


## 📤 FastAPI Endpoints
POST /analyze-invoices/
Inputs: HR policy PDF, ZIP file of invoice PDFs, employee name

Output: JSON list of reimbursement decisions

POST /chat-query/
Input: Query string (e.g. "What invoices were declined for Sahil?")

Output: Markdown-based LLM response from stored invoice metadata

## 🔒 Redundancy & Stability
✅ LLM Fallback: Gemini 2.0 Flash → LLaMA3 via Groq

✅ PDF Fallback: PyMuPDF → pdfplumber

✅ ZIP Fallback: zipfile → shutil

✅ Batch Processing: ThreadPoolExecutor-based processing

✅ Logging: All steps/errors in logs/app.log

## 🧠 Author
Built with ❤️ by Sahil Dinesh Rahate

Open to suggestions, improvements, and collaborations!