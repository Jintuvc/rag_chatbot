import re
from deep_translator import GoogleTranslator

# ------------------------------
# Language Maps
# ------------------------------
LANG_MAP = {
    6: "Hindi",
    7: "Kannada",
    11: "Malayalam",
    20: "Tamil",
    21: "Telugu",
    24: "English",
}

LANG_CODE_MAP = {
    "hindi": "hi",
    "kannada": "kn",
    "malayalam": "ml",
    "tamil": "ta",
    "telugu": "te",
    "english": "en"
}


# ------------------------------
# Script Detection (Regex ranges)
# ------------------------------
def is_malayalam(text: str) -> bool:
    return bool(re.search(r'[\u0D00-\u0D7F]', text))

def is_hindi(text: str) -> bool:
    return bool(re.search(r'[\u0900-\u097F]', text))

def is_kannada(text: str) -> bool:
    return bool(re.search(r'[\u0C80-\u0CFF]', text))

def is_telugu(text: str) -> bool:
    return bool(re.search(r'[\u0C00-\u0C7F]', text))

def is_tamil(text: str) -> bool:
    return bool(re.search(r'[\u0B80-\u0BFF]', text))


# ------------------------------
# Dataset Helpers
# ------------------------------
def parse_language_codes(codes_str: str):
    """
    Dataset has comma-separated codes like "24,20".
    Returns list of readable language names.
    """
    try:
        codes = [int(c.strip()) for c in str(codes_str).split(",") if c.strip()]
    except:
        codes = []
    return [LANG_MAP.get(c) for c in codes if c in LANG_MAP]


def filter_by_language_code(df, code):
    """
    Filter dataset by released language code.
    Uses 'Released Languages' column.
    """
    return df[df["Released Languages"].astype(str).str.contains(rf"\b{code}\b", case=False, na=False)]


# ------------------------------
# Translation Helper
# ------------------------------
def translate_answer(answer: str, user_query: str) -> str:
    """
    Detect query language → translate answer into that language.
    """
    target_lang = "en"

    if is_hindi(user_query):
        target_lang = "hi"
    elif is_kannada(user_query):
        target_lang = "kn"
    elif is_malayalam(user_query):
        target_lang = "ml"
    elif is_tamil(user_query):
        target_lang = "ta"
    elif is_telugu(user_query):
        target_lang = "te"

    if target_lang == "en":
        return answer  # no translation needed

    try:
        return GoogleTranslator(source="en", target=target_lang).translate(answer)
    except Exception as e:
        print(f"Translation failed: {e}")
        return answer
