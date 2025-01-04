import streamlit as st
from functions.check_api import check_openai_api_key

# Page configuration
st.set_page_config(page_title="Practice LangChain Apps", 
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

st.subheader('About')
st.write('''
This app showcases a collection of small, practice applications built with LangChain, OpenAI, Serper API, Pinecone, and Streamlit. 
- **LangChain**: Provides the logic for connecting and orchestrating applications.  
- **OpenAI**: Utilizes `gpt-4o-mini` for the LLM and `text-embedding-3-large` for embeddings.  
- **Pinecone**: Handles vector embedding storage and search.  
- **Serper API**: Enables internet search functionality.  
- **Streamlit**: Serves as the framework for building the web app.
''')


st.subheader('Gift Idea Assistant')
st.write('Find unique gift ideas by searching the internet using the Serper API.')

st.subheader('Research Paper Assistant')
st.write('Upload a PDF to explore and ask detailed questions about its content.')

st.subheader('YouTube Assistant')
st.write('Paste a YouTube video link to ask questions and gain insights from the video.')

