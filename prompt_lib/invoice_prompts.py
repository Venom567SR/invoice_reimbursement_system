from langchain_core.prompts import ChatPromptTemplate

invoice_prompt = ChatPromptTemplate.from_template("""
You are an HR compliance assistant. Based on the following HR reimbursement policy and an employee invoice, determine:
1. Whether it is fully reimbursed, partially reimbursed, or declined.
2. Explain the reason clearly.

Respond in this format:
Status: <One of [Fully Reimbursed, Partially Reimbursed, Declined]>
Reason: <Justification in 1–2 sentences>

[Policy Text]:
{policy_text}

[Invoice Text]:
{invoice_text}

[Employee Name]: {employee}
""")