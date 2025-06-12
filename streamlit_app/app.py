import streamlit as st
import requests
import json
import os

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Invoice Reimbursement System", layout="wide")

# Load custom CSS
def inject_custom_css():
    try:
        with open("static/styles/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Custom CSS not found. Default styling will be used.")

inject_custom_css()

st.title("🧾 Invoice Reimbursement System")

tab1, tab2, tab3 = st.tabs([
    "🔍 Analyze Invoices",
    "💬 Query Chatbot",
    "📂 View Last Results"
])

# ------------------------- TAB 1: Analyze -------------------------
with tab1:
    st.header("Upload HR Policy PDF and Invoice ZIP")

    with st.form("upload_form"):
        policy_pdf = st.file_uploader("Upload HR Policy PDF", type="pdf")
        invoices_zip = st.file_uploader("Upload ZIP of Invoice PDFs", type="zip")
        employee_name = st.text_input("Employee Name")
        submitted = st.form_submit_button("Analyze Invoices")

    if submitted:
        if not (policy_pdf and invoices_zip and employee_name):
            st.error("❌ All fields are required.")
        else:
            with st.spinner("Analyzing invoices..."):
                files = {
                    "policy_pdf": ("policy.pdf", policy_pdf, "application/pdf"),
                    "invoices_zip": ("invoices.zip", invoices_zip, "application/zip")
                }
                data = {"employee_name": employee_name}
                try:
                    response = requests.post(f"{API_URL}/analyze-invoices/", files=files, data=data)
                    result = response.json()

                    if isinstance(result, list) and result:
                        st.success(f"✅ {len(result)} invoice(s) processed.")
                        for res in result:
                            st.markdown(f"""#### 📄 Invoice: `{res["invoice_id"]}`
- **Status**: `{res["status"]}`
- **Reason**: {res["reason"]}
- **Employee**: {res["employee"]}
- **Date**: {res["date"]}
---""")
                    elif isinstance(result, list) and not result:
                        st.warning("⚠️ No invoices were processed. ZIP might be empty or unreadable.")
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                except Exception as e:
                    st.exception(e)

# ------------------------- TAB 2: Chatbot -------------------------
with tab2:
    st.header("Ask a Question About Past Reimbursements")

    query = st.text_input("🔎 Enter your query")
    if st.button("Ask"):
        if not query:
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(f"{API_URL}/chat-query/", data={"query": query})
                    result = response.json()
                    if result.get("success"):
                        st.markdown(result["response"])
                    else:
                        st.error(result.get("error", "Unknown error"))
                except Exception as e:
                    st.exception(e)

# ------------------------- TAB 3: Preview Last Results -------------------------
with tab3:
    st.header("📂 Previously Analyzed Invoices")
    if os.path.exists("static/results.json"):
        with open("static/results.json", "r") as f:
            results = json.load(f)

        if results:
            for res in results:
                st.markdown(f"""#### 📄 Invoice: `{res["invoice_id"]}`
- **Status**: `{res["status"]}`
- **Reason**: {res["reason"]}
- **Employee**: {res["employee"]}
- **Date**: {res["date"]}
---""")
        else:
            st.info("No previous results found in file.")
    else:
        st.info("results.json not found.")