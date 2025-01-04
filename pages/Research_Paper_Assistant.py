import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import functions.research_helper as lch
from functions.check_api import check_openai_api_key
from io import BytesIO
from functions.generate_unique_id import generate_unique_id

st.set_page_config(page_title="Research Paper Assistant", 
                   page_icon="📝",
                   layout="wide")

st.markdown("<h1 style='text-align: center; color: #57cfff;'>Research Paper Helper</h1>", unsafe_allow_html=True)

check_openai_api_key(st.session_state)

pdf_file = st.file_uploader('Upload PDF', type='pdf')

example_pdf_file = st.selectbox('Select an Example Paper', ['TikTok Recommendor System', 'Retrieval-Augmented Generation', 'TensorFlow'], index=None)

if example_pdf_file == 'TikTok Recommendor System':
  with open('example_PDFs/TikTok_white_paper.pdf', 'rb') as f:
    pdf_file = BytesIO(f.read())
elif example_pdf_file == 'Retrieval-Augmented Generation':
  with open('example_PDFs/RAG_white_paper.pdf', 'rb') as f:
    pdf_file = BytesIO(f.read())
elif example_pdf_file == 'TensorFlow':
  with open('example_PDFs/TensorFlow_white_paper.pdf', 'rb') as f:
    pdf_file = BytesIO(f.read())

if pdf_file:
  binary_data = pdf_file.read()
  id_pdf_file = generate_unique_id()

  pdf_viewer(input=binary_data, width=1200)

else:
    st.write("Please upload a PDF or select an example paper.")

with st.sidebar:
    with st.form("input_form"):
      question_input = st.text_area('Your Question')
      submit_button = st.form_submit_button('Submit')

    if submit_button:
      if pdf_file:
        st.header('Response')
        db = lch.add_pdf_to_db(pdf_file, id_pdf_file)
        response = lch.get_response_from_query(db, question_input, id_pdf_file)      
        st.write(response.content)
      else:
         st.write('Upload a PDF first!')





  


