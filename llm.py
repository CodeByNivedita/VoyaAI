from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

GOOGLE_API_KEY = (
    st.secrets.get("GOOGLE_API_KEY")
    or os.getenv("GOOGLE_API_KEY")
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    google_api_key=GOOGLE_API_KEY,
)