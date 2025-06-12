import os

# Folder structure
FOLDERS = [
    "data/raw_zips",
    "data/extracted_invoices",
    "logs",
    "static/styles",
    "streamlit_app",
    "prompt_lib",
    "utils",
    "vector_db",
]

# Files to create with optional boilerplate content
FILES = {
    "README.md": "# Invoice Reimbursement System\n\nGenerated project structure.",
    "requirements.txt": "# Dependencies will be added here.",
    "config.yaml": "# Configuration settings go here.",
    "setup.py": "# Optional setup file for packaging.",
    "main.py": "# Entry point or orchestrator.",
    "app.py": "# FastAPI application entry point.",
    "static/results.json": "{}",
    "static/styles/style.css": "/* Custom Streamlit styles */",
    "streamlit_app/app.py": "# Streamlit testing interface",
    "prompt_lib/invoice_prompts.py": "# Prompts for invoice analysis",
    "prompt_lib/chatbot_prompts.py": "# Prompts for chatbot",
    "utils/logger.py": "# Logging utility setup",
    "utils/exceptions.py": "# Custom exceptions and error codes",
    "utils/zip_handler.py": "# ZIP extraction logic",
    "utils/pdf_parser.py": "# PDF parsing logic with fallback",
    "utils/batch_processor.py": "# Multiprocessing/threading invoice handler",
    "utils/embedding.py": "# Embedding generation logic",
    "utils/llm_utils.py": "# LLM interface with fallback",
    "utils/config.py": "# YAML + env configuration loader",
    "vector_db/chromadb_utils.py": "# ChromaDB utility functions",
}

# Automatically add __init__.py to package folders
PACKAGE_FOLDERS = [
    "data", "data/raw_zips", "data/extracted_invoices",
    "logs", "static", "static/styles",
    "streamlit_app", "prompt_lib", "utils", "vector_db"
]


def create_structure():
    for folder in FOLDERS:
        os.makedirs(folder, exist_ok=True)

    for package in PACKAGE_FOLDERS:
        init_path = os.path.join(package, "__init__.py")
        with open(init_path, "w") as f:
            f.write("# Package init\n")

    for path, content in FILES.items():
        with open(path, "w") as f:
            f.write(content)

    print("✅ Project structure created successfully.")


if __name__ == "__main__":
    create_structure()