from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import os
import shutil
from datetime import datetime
import json

from utils.logger import app_logger
from utils.exceptions import (
    InvoiceSystemException, PDFParsingError, ZipExtractionError, ValidationError, ErrorCodes
)
from utils.pdf_parser import parse_pdf_with_fallback
from utils.zip_handler import extract_zip_with_fallback
from utils.embedding import get_embedding_model
from utils.llm_utils import run_llm_with_fallback
from prompt_lib.invoice_prompts import invoice_prompt
from prompt_lib.chatbot_prompts import chatbot_query_prompt
from vector_db.chromadb_utils import get_chroma_db, add_invoice_to_vector_store
from utils.batch_processor import process_invoices_in_parallel
from utils.config import get_config

app = FastAPI()
config = get_config()


@app.exception_handler(InvoiceSystemException)
async def handle_custom_exception(request, exc: InvoiceSystemException):
    return JSONResponse(status_code=400, content={
        "success": False,
        "error": exc.message,
        "error_code": exc.error_code
    })


@app.post("/analyze-invoices/")
async def analyze_invoices(
    policy_pdf: UploadFile = File(...),
    invoices_zip: UploadFile = File(...),
    employee_name: str = Form(...)
):
    try:
        os.makedirs("temp", exist_ok=True)
        policy_path = os.path.join("temp", policy_pdf.filename)
        zip_path = os.path.join("temp", invoices_zip.filename)

        with open(policy_path, "wb") as f:
            shutil.copyfileobj(policy_pdf.file, f)
        with open(zip_path, "wb") as f:
            shutil.copyfileobj(invoices_zip.file, f)

        app_logger.info("Parsing HR policy...")
        policy_text = parse_pdf_with_fallback(policy_path)

        app_logger.info("Extracting ZIP invoices...")
        extract_zip_with_fallback(zip_path, "data/extracted_invoices")

        invoice_files = [
            os.path.join("data/extracted_invoices", f)
            for f in os.listdir("data/extracted_invoices")
            if f.endswith(".pdf")
        ]

        if not invoice_files:
            raise ValidationError("No PDF invoices found in the ZIP.", ErrorCodes.FILE_NOT_FOUND)

        embedding_model = get_embedding_model()
        vector_store = get_chroma_db(embedding_model)

        def process_invoice(file_path):
            invoice_id = os.path.basename(file_path)
            app_logger.info(f"Processing invoice: {invoice_id}")

            invoice_text = parse_pdf_with_fallback(file_path)
            if not invoice_text.strip():
                raise PDFParsingError(f"No text extracted from {invoice_id}")

            response = run_llm_with_fallback(invoice_prompt, {
                "policy_text": policy_text,
                "invoice_text": invoice_text,
                "employee": employee_name
            })

            print(f"\n📄 {invoice_id} — LLM Response:\n{response}\n")
            app_logger.info(f"LLM response for {invoice_id}: {response}")

            try:
                status_line = next(line for line in response.splitlines() if line.startswith("Status:"))
                reason_line = next(line for line in response.splitlines() if line.startswith("Reason:"))
                status = status_line.replace("Status:", "").strip()
                reason = reason_line.replace("Reason:", "").strip()
            except Exception:
                raise PDFParsingError("LLM returned an invalid format")

            metadata = {
                "invoice_id": invoice_id,
                "employee": employee_name,
                "status": status,
                "reason": reason,
                "date": str(datetime.today().date())
            }

            add_invoice_to_vector_store(vector_store, invoice_text + " " + reason, metadata)
            app_logger.info(f"Stored in ChromaDB: {metadata}")

            return {
                "success": True,
                **metadata
            }

        results = process_invoices_in_parallel(process_invoice, invoice_files)

        # Optional: write to static/results.json
        with open("static/results.json", "w") as f:
            json.dump(results, f, indent=2)

        return results

    except InvoiceSystemException as e:
        raise e
    except Exception as e:
        app_logger.exception("Unhandled error in /analyze-invoices")
        raise InvoiceSystemException(str(e), "API_001")


@app.post("/chat-query/")
async def chat_query(query: str = Form(...)):
    try:
        embedding_model = get_embedding_model()
        vector_store = get_chroma_db(embedding_model)

        app_logger.info(f"Performing vector search for query: {query}")
        results = vector_store.similarity_search(query, k=5)

        if not results:
            app_logger.warning("No results found in vector DB.")
            return {
                "success": True,
                "response": "No matching invoice records found in the database."
            }

        context = "\n\n".join([
            f"Invoice: {doc.metadata.get('invoice_id')}\nEmployee: {doc.metadata.get('employee')}\nStatus: {doc.metadata.get('status')}\nReason: {doc.metadata.get('reason')}\nDate: {doc.metadata.get('date')}"
            for doc in results
        ])

        response = run_llm_with_fallback(chatbot_query_prompt, {
            "query": query,
            "context": context
        })

        app_logger.info("Chatbot response generated successfully.")
        return {
            "success": True,
            "response": response
        }

    except InvoiceSystemException as e:
        raise e
    except Exception as e:
        app_logger.exception("Unhandled error in /chat-query")
        raise InvoiceSystemException(str(e), "API_002")