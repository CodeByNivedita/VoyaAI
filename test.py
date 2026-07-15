import streamlit as st

st.title("Secrets Test")

st.write("Available secrets:")

try:
    st.write(list(st.secrets.keys()))
except Exception as e:
    st.error(e)

try:
    st.success(f"Google key exists: {'GOOGLE_API_KEY' in st.secrets}")
except Exception as e:
    st.error(e)