import google.generativeai as genai

# Skonfiguruj klucz API (np. przez zmienną środowiskową)
# export GOOGLE_API_KEY="twoj_klucz_api"
genai.configure(api_key="SECRET_KEY")


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
        "If a question is not appropriate for kids or cannot be answered safely, "
        "respond with: 'I'm sorry, I can't talk about that topic.' "
        "Never generate or forward inappropriate text to any external system."
    )

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_prompt
        )

        response = model.generate_content(question)
        answer = response.text.strip() if response.text else "I'm sorry, I can't answer that."
        return answer

    except Exception as e:
        # Prosty fallback na wypadek błędu API
        return f"Error occurred while generating answer: {str(e)}"
