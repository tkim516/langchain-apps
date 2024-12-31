import streamlit as st
import functions.youtube_helper as lch
from functions.check_api import check_openai_api_key

st.set_page_config(page_title="YouTube Assistant", 
                   page_icon="🤖",
                   layout="wide")

st.markdown("<h1 style='text-align: center; color: #57cfff;'>YouTube Assistant</h1>", unsafe_allow_html=True)

# Check if API key is stored in session state
check_openai_api_key(st.session_state)

with st.sidebar.form("input_form"):
    url_input = st.text_area('Youtube Video URL')
    question_input = st.text_area('Your Question')
    submit_button = st.form_submit_button('Submit')

if submit_button:
  st.header('Response')
  db = lch.add_transcipt_to_db(url_input)
  response = lch.get_response_from_query(db, question_input, url_input)
  st.write(response.content)

  


