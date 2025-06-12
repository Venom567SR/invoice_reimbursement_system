from langchain_core.prompts import ChatPromptTemplate

chatbot_query_prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant. Answer the following query using the context of previously analyzed invoice data.

Query: {query}

Context:
{context}

Respond in Markdown format.
""")