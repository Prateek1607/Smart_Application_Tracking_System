import os
import streamlit as st
import google.generativeai as genai

def get_model():
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY") or st.secrets["GOOGLE_API_KEY"]
    except Exception:
        api_key = st.secrets["GOOGLE_API_KEY"]

    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        generation_config=genai.GenerationConfig(temperature=0)
    )