import streamlit as st
from functions.check_api import check_openai_api_key

# Page configuration
st.set_page_config(page_title="Tyler's LangChain Apps", 
                   page_icon="",
                   layout="wide")

st.markdown("<h1 style='text-align: center; color: #57cfff;'>Tyler's LangChain Apps</h1>", unsafe_allow_html=True)

# Check if API key is stored in session state
check_openai_api_key(st.session_state)
