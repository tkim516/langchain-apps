import openai
import streamlit as st
import time

def check_openai_api_key(session_state):
    if 'OPENAI_API_KEY' not in session_state:
        st.session_state['OPENAI_API_KEY'] = None

    def validate_key(api_key):
        openai.api_key = api_key  # Explicitly set the key in openai's config
        try:
            openai.Model.list()  # Use `openai.Model.list()` instead of client instantiation
        except openai.error.AuthenticationError:
            return False
        else:
            return True

    if st.session_state['OPENAI_API_KEY'] is None:
        open_api_key = st.text_area('Enter your OpenAI API Key')
        submit_button = st.button('Submit')

        if submit_button and open_api_key:
            if validate_key(open_api_key):
                st.session_state['OPENAI_API_KEY'] = open_api_key
                openai.api_key = open_api_key  # Ensure the key is globally set
                st.success("API key successfully stored!")
                time.sleep(1)
                st.rerun()  # Updated to the latest Streamlit rerun API

            else:
                st.error("Invalid OpenAI API Key. Please try again.")

    else:
        st.subheader(f"Using OpenAI Key: {st.session_state['OPENAI_API_KEY'][0:10]}......")
        openai.api_key = st.session_state['OPENAI_API_KEY']  # Ensure key is always set for openai
