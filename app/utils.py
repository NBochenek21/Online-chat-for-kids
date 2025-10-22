import google.generativeai as genai
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)


def call_llm(question: str) -> str:
    """Generates API call to Gemini 1.5 Flash and returns filtered child-safe response.

    Args:
        question (str): Question to be answered by LLM, asked by a kid.

    Returns:
        str: Safe, simplified and kind answer.
    """
    system_prompt = (
        "You are a friendly and safe assistant for kids aged 6–12. "
        "Answer simply, kindly, and factually. "
        "Avoid any adult, violent, political, or sensitive content. "
        "You must anwer questions related to animals, fairytales and colours. "
        "If a question is related to other topic reply: I cant't answer that question. Ask me anything about animals, fairytales or colours.  "
    )

    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=system_prompt
        )

        response = model.generate_content(question)
        answer = response.text.strip() if response.text else "I'm sorry, I can't answer that."
        return answer

    except Exception as e:
        # Prosty fallback na wypadek błędu API
        return f"Error occurred while generating answer: {str(e)}"
    

print(call_llm("What is the biggest animal?")) 
