from utils.pdf_parser import parse_pdf_with_fallback
from utils.llm_utils import run_llm_with_fallback
from utils.embedding import get_embedding_model
from vector_db.chromadb_utils import get_chroma_db, add_invoice_to_vector_store
from prompt_lib.invoice_prompts import invoice_prompt
from datetime import datetime

def main():
    policy_text = parse_pdf_with_fallback("data/policy.pdf")
    invoice_text = parse_pdf_with_fallback("data/extracted_invoices/sample.pdf")
    employee = "Sahil"

    response = run_llm_with_fallback(invoice_prompt, {
        "policy_text": policy_text,
        "invoice_text": invoice_text,
        "employee": employee
    })

    print("\n--- LLM RESPONSE ---")
    print(response)

    # Store in vector DB
    embedding = get_embedding_model()
    db = get_chroma_db(embedding)
    add_invoice_to_vector_store(db, invoice_text + response, {
        "invoice_id": "sample.pdf",
        "employee": employee,
        "status": "Manual",
        "reason": "Testing CLI mode",
        "date": str(datetime.today().date())
    })

if __name__ == "__main__":
    main()