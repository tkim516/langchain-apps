import streamlit as st
import functions.gift_generator_helper as lch
from functions.check_api import check_openai_api_key
from langchain_community.utilities import GoogleSerperAPIWrapper
import os


st.set_page_config(page_title="Gift Idea Assistant", 
                   page_icon="🎁",
                   layout="wide")

st.markdown("<h1 style='text-align: center; color: #57cfff;'>Gift Idea Assistant</h1>", unsafe_allow_html=True)

check_openai_api_key(st.session_state)
api_key = st.session_state['OPENAI_API_KEY']

serper_api_key = os.environ.get('SERPER_API_KEY', '')
if not serper_api_key:
    raise ValueError("SERPER_API_KEY environment variable is not set.")



with st.sidebar.form("input_form"):
    recipient_hobbies = st.text_input("Recipient's Hobbies", placeholder="Reading, Cooking")
    recipient_age = st.number_input("Recipient's Age", min_value=0, max_value=120, value=20, step=1)
    budget = st.text_input("Budget (USD)", placeholder="$50-$100")
    submit_button = st.form_submit_button('Generate Gift Suggestions')

if submit_button:
  try:
    response = lch.generate_gift_search_query(recipient_hobbies, recipient_age, budget, api_key)
    st.subheader("Gift Suggestions")

    search_result = lch.serper_shopping_search(serper_api_key, response.content).json()
    products = search_result["shopping"]
    first_five_products = products[:5]

    for product in first_five_products:
      title = product.get('title', 'No title available')
      link = product.get('link', 'No link available')
      price = product.get('price', 'No price available')
      
      st.write(f"Title: {title}")
      st.write(f"Link: {link}")
      st.write(f"Price: {price}")
      st.write('---')

  except Exception as e:
    st.error(f"An error occurred: {e}")
