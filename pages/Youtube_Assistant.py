import streamlit as st
import functions.youtube_helper as lch
from functions.check_api import check_openai_api_key

st.set_page_config(page_title="YouTube Assistant", 
                   page_icon="🎥",
                   layout="wide")

st.markdown("<h1 style='text-align: center; color: #57cfff;'>YouTube Assistant</h1>", unsafe_allow_html=True)

# Check if API key is stored in session state
check_openai_api_key(st.session_state)

with st.sidebar.form("input_form"):
    url_input = st.text_area('Youtube Video URL', value='https://www.youtube.com/watch?v=aywZrzNaKjs')
    question_input = st.text_area('Your Question', value='What is the video about?')
    submit_button = st.form_submit_button('Submit')

if submit_button:
  st.write(f'Video URL: {url_input}')
  db = lch.add_transcipt_to_db(url_input)
  response = lch.get_response_from_query(db, question_input, url_input)
  st.header('Response')
  st.write(response.content)

  


