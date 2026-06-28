import json
import re
from decouple import config

try:
    from google import genai
except ImportError:
    genai = None


GEMINI_API_KEY = config("GEMINI_API_KEY", default="")
GEMINI_MODEL = config("GEMINI_MODEL", default="gemini-3.5-flash")


def is_gemini_configured():
    if genai is None:
        return False

    if not GEMINI_API_KEY:
        return False

    if GEMINI_API_KEY in ["your_gemini_api_key", "your_actual_gemini_api_key"]:
        return False

    return True


def call_gemini(prompt):
    if not is_gemini_configured():
        return {
            "success": False,
            "text": "",
            "error": "Gemini API key is not configured properly."
        }

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        interaction = client.interactions.create(
            model=GEMINI_MODEL,
            input=prompt
        )

        response_text = getattr(interaction, "output_text", "")

        return {
            "success": True,
            "text": response_text,
            "error": None
        }

    except Exception as error:
        return {
            "success": False,
            "text": "",
            "error": str(error)
        }


def extract_json_from_text(text):
    if not text:
        return None

    cleaned_text = text.strip()

    cleaned_text = re.sub(
        r"^```json\s*",
        "",
        cleaned_text,
        flags=re.IGNORECASE
    )

    cleaned_text = re.sub(
        r"^```\s*",
        "",
        cleaned_text
    )

    cleaned_text = re.sub(
        r"\s*```$",
        "",
        cleaned_text
    )

    start_index = cleaned_text.find("{")
    end_index = cleaned_text.rfind("}")

    if start_index == -1 or end_index == -1:
        return None

    json_text = cleaned_text[start_index:end_index + 1]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        return None