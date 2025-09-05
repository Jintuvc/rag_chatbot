import os
import streamlit as st
import pandas as pd
import re
from deep_translator import GoogleTranslator   # 🔥 NEW

from indexer import build_or_load_index, load_dataset
from rag import retrieve, answer_from_hits, list_courses_in_language
from utils import LANG_MAP
from map import search_places  # ✅ external tool

# ------------------------------
# Script detection (for languages)
# ------------------------------
def is_malayalam(text):
    return bool(re.search(r'[\u0D00-\u0D7F]', text))

def is_hindi(text):
    return bool(re.search(r'[\u0900-\u097F]', text))

def is_kannada(text):
    return bool(re.search(r'[\u0C80-\u0CFF]', text))

def is_telugu(text):
    return bool(re.search(r'[\u0C00-\u0C7F]', text))

def is_tamil(text):
    return bool(re.search(r'[\u0B80-\u0BFF]', text))


# ------------------------------
# 🔥 Language Translation Helper
# ------------------------------
def translate_answer(answer: str, user_query: str) -> str:
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


# ------------------------------
# Load Dataset + Index
# ------------------------------
DATA_PATH = r"boss_wallah_rag_bot.csv"

st.set_page_config(page_title="Boss Wallah RAG Support Bot", page_icon="🧱", layout="wide")
st.title("Boss Wallah – Course Support Chatbot (RAG + Agentic)")

@st.cache_resource
def load_everything():
    raw_df = load_dataset(DATA_PATH)
    meta, index, model = build_or_load_index(DATA_PATH)
    return raw_df, meta, index, model

raw_df, meta_df, index, model = load_everything()


# ------------------------------
# Sidebar
# ------------------------------
st.sidebar.header("Quick Actions")
st.sidebar.text("Use the buttons below to quickly test queries.")


# ------------------------------
# Dataset Answer
# ------------------------------
def dataset_only_answer(user_query: str):
    lower = user_query.lower()
    lang_hit = None
    for code, name in LANG_MAP.items():
        if name.lower() in lower:
            lang_hit = code
            break
    if lang_hit is not None:
        ans = list_courses_in_language(raw_df, lang_hit)
    else:
        hits = retrieve(user_query, index, model, meta_df, k=5)
        ans = answer_from_hits(hits, raw_df, user_query)

    # 🔥 Translate final dataset answer
    if isinstance(ans, str):
        return translate_answer(ans, user_query)
    elif isinstance(ans, list):
        for r in ans:
            for k, v in r.items():
                if isinstance(v, str):
                    r[k] = translate_answer(v, user_query)
        return ans
    else:
        return ans


def dataset_or_bonus_answer(user_query: str):
    lower = user_query.lower()

    # Special dairy farm rule
    dairy_keywords = [
        "cow", "cows", "dairy farm",
        "பால்", "பசுக்கள்",        # Tamil
        "ಡೈರಿ", "ಹಸುಗಳು",         # Kannada
        "डेयरी", "गायें",          # Hindi
        "డైరీ", "ఆవులు",          # Telugu
        "ഡയറി", "പശുക്കൾ"          # Malayalam
    ]

    if any(word in lower for word in dairy_keywords):
        hits = retrieve("dairy farm cows needed " + user_query, index, model, meta_df, k=5)
        ans = answer_from_hits(hits, raw_df, user_query)

        nums = re.findall(r"\b\d+\b", str(ans))
        if nums:
            return nums[0]
        else:
            # Language-specific fallback
            if is_hindi(user_query):
                return "डेटासेट में स्पष्ट नहीं है।"
            elif is_kannada(user_query):
                return "ಡೇಟಾಸೆಟ್‌ನಲ್ಲಿ ನಿರ್ದಿಷ್ಟಪಡಿಸಲಾಗಿಲ್ಲ."
            elif is_malayalam(user_query):
                return "ഡാറ്റാസെറ്റിൽ വ്യക്തമാക്കിയിട്ടില്ല."
            elif is_tamil(user_query):
                return "தரவுத்தொகுப்பில் குறிப்பிடப்படவில்லை."
            elif is_telugu(user_query):
                return "డేటాసెట్‌లో స్పష్టంగా లేదు."
            else:
                return "Information not specified in the dataset."

    return dataset_only_answer(user_query)


# ------------------------------
# Router: Decide Dataset or Maps
# ------------------------------
def route_query(user_query: str):
    outside_keywords = ["store", "shop", "temple", "hospital", "university",
                        "college", "market", "restaurant", "mall", "hotel"]
    if any(word in user_query.lower() for word in outside_keywords):
        return "maps"
    return "dataset"


# ------------------------------
# Display Answer
# ------------------------------
def display_answer(answer):
    if isinstance(answer, dict) or isinstance(answer, list):
        df = pd.DataFrame(answer)
        df = df.reset_index(drop=True)
        if "Who This Course Is For" in df.columns:
            df["Who This Course Is For"] = df["Who This Course Is For"].apply(
                lambda x: "\n".join([f"- {part.strip()}" for part in str(x).split("|||")])
            )
        st.table(df)
    else:
        st.write(answer)


# ------------------------------
# Main Query Handling
# ------------------------------
query = st.text_input("Ask about Boss Wallah courses or local info:",
                      placeholder="e.g., Tell me about honey bee farming course OR papaya seeds store in Coimbatore")
go = st.button("Ask")

if go and query.strip():
    st.subheader("Answer")
    route = route_query(query)

    if route == "dataset":
        answer = dataset_or_bonus_answer(query)
        display_answer(answer)
    elif route == "maps":
        results = search_places(query)
        if isinstance(results, list):
            st.table(results)
        else:
            st.write(results)
