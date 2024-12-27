import streamlit as st
import functions.gift_generator_helper as lch
from functions.check_api import check_openai_api_key

st.set_page_config(page_title="Gift Idea Assistant", 
                   page_icon="🎁",
                   layout="wide")

st.markdown("<h1 style='text-align: center; color: #57cfff;'>Gift Idea Assistant</h1>", unsafe_allow_html=True)

check_openai_api_key(st.session_state)

with st.sidebar.form("input_form"):
    recipient_hobbies = st.text_input("Recipient's Hobbies", placeholder="Reading, Cooking")
    recipient_age = st.number_input("Recipient's Age", min_value=0, max_value=120, value=20, step=1)
    relationship = st.text_input("Your Relationship to the Recipient", placeholder="Friend, Family Member")
    occasion = st.text_input("Occasion", placeholder="Birthday, Anniversary")
    budget = st.text_input("Budget (USD)", placeholder="$50-$100")
    submit_button = st.form_submit_button('Generate Gift Suggestions')

if submit_button:
  try:
    response = lch.generate_gifts(recipient_hobbies, recipient_age, relationship, occasion, budget, api_key)
    st.success("Gift Suggestions:")
    st.write(response.content)
  except Exception as e:
    st.error(f"An error occurred: {e}")
