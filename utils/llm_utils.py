from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from utils.config import get_config
from utils.exceptions import LLMError, LLMConnectionError, LLMResponseError, handle_exception
from utils.logger import app_logger

config = get_config()

@handle_exception
def get_gemini_llm():
    try:
        return ChatGoogleGenerativeAI(model=config["llm"]["primary_model"], temperature=0.2)
    except Exception as e:
        raise LLMConnectionError(f"Failed to connect to Gemini: {str(e)}")

@handle_exception
def get_llama3_llm():
    try:
        return ChatGroq(model=config["llm"]["fallback_model"], temperature=0.2)
    except Exception as e:
        raise LLMConnectionError(f"Failed to connect to Groq: {str(e)}")

@handle_exception
def run_llm_with_fallback(prompt_template: ChatPromptTemplate, input_data: dict) -> str:
    output_parser = StrOutputParser()

    try:
        app_logger.info("Trying Gemini 2.0 Flash via Google...")
        llm = get_gemini_llm()
        chain = prompt_template | llm | output_parser
        return chain.invoke(input_data)
    except LLMError:
        app_logger.warning("Gemini failed, trying LLaMA3 via Groq...")
        try:
            llm = get_llama3_llm()
            chain = prompt_template | llm | output_parser
            return chain.invoke(input_data)
        except Exception as e:
            raise LLMResponseError(f"LLM fallback also failed: {str(e)}")