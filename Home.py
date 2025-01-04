import streamlit as st
from functions.check_api import check_openai_api_key

# Page configuration
st.set_page_config(page_title="Tyler's LangChain Apps", 
                   page_icon="",
                   layout="wide")

st.markdown("<h1 style='text-align: center; color: #57cfff;'>Tyler's LangChain Apps</h1>", unsafe_allow_html=True)

# Check if API key is stored in session state
check_openai_api_key(st.session_state)

import os
from pinecone import Pinecone

pinecone_api_key = os.environ.get('PINECONE_API_KEY', '')
if not pinecone_api_key:
    raise ValueError("PINECONE_API_KEY environment variable is not set.")

st.header('Research Paper Assistant')
st.subheader('Upload a PDF and ask questions about the paper. Built with LangChain and Pinecone')

st.header('YouTube Assisstant')
st.subheader('Copy a YouTube video link and ask questions about the video. The video transcript is embedded and loaded into the Pinecone database.')
