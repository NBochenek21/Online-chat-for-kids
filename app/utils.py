import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def call_llm(question: str, model_name: str | None = None) -> str:
    """Generate a child-safe response using the configured generative model.

    The model can be chosen via the LLM_MODEL environment variable or passed
    directly. If the selected model is not available this function will attempt
    to return a short diagnostic listing available models.
    """
    system_prompt = (
        "You are a friendly and safe assistant for kids aged 6–12. "
        "There are only 3 topics you can talk about: animals, colours and school. "
        "If the question is outside these topics, even if it seems innocent, "
        "respond with: 'I'm sorry, I can't talk about that topic.' "
        " REMEBER TO STAY WITHIN THESE TOPICS ONLY. "
    )

    model_name = model_name or os.getenv("LLM_MODEL") or "gemini-2.0-flash"

    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt,
        )
        response = model.generate_content(question)
        text = getattr(response, "text", None)
        if text:
            return text.strip()
        return str(response)

    except Exception as e:
        err = str(e)
        return f"Error occurred while generating answer: {err}"


if __name__ == "__main__":
    example = "What is the capital of France?"
    print(call_llm(example))
