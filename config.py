import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient

load_dotenv()

GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = st.secrets.get("TAVILY_API_KEY") or os.getenv("TAVILY_API_KEY")
OPENWEATHER_API_KEY = st.secrets.get("OPENWEATHER_API_KEY") or os.getenv("OPENWEATHER_API_KEY")
UNSPLASH_ACCESS_KEY = st.secrets.get("UNSPLASH_ACCESS_KEY") or os.getenv("UNSPLASH_ACCESS_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)

tavily = TavilyClient(api_key=TAVILY_API_KEY)