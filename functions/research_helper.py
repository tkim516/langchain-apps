from langchain.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_community.document_loaders import PyPDFLoader
from tempfile import NamedTemporaryFile
import os
import streamlit as st


def add_pdf_to_db(uploaded_file):
  embeddings = OpenAIEmbeddings(
      model="text-embedding-3-large",
      openai_api_key=os.environ.get("OPENAI_API_KEY")
  )

  pc = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))
  index_name = "pdf-embeddings"
  index = pc.Index(index_name)
  vector_store = PineconeVectorStore(embedding=embeddings, index=index)

  with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_file_path = temp_file.name

  try:
        # Use the temporary file path with PyPDFLoader
        loader = PyPDFLoader(temp_file_path)
        pages = []
        for page in loader.lazy_load():
            pages.append(page)

        # Split the PDF into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True
        )
        all_splits = text_splitter.split_documents(pages)

        # Add the chunks to the vector store
        _ = vector_store.add_documents(documents=all_splits)

        return vector_store
  finally:
        # Clean up: delete the temporary file
        os.remove(temp_file_path)

def get_response_from_query(vector_store, query, k=4):
  retrieved_docs = vector_store.similarity_search(query, k=k)
  retrieved_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

  llm = ChatOpenAI(model="gpt-4o-mini")

  prompt = PromptTemplate(
    input_variables=['question, context'],
    template="""
    You are an assistant that answers questions based on the information in the uploaded PDF.

    Answer this question: {question}

    Use this segment of the uploaded PDF: {context}

    If you do not have enough information to answer the question, reply with "I don't have enough information to answer your question.".
    """
  )

  message = prompt.invoke({
    'question': query,
    'context': retrieved_content})
  
  response = llm.invoke(message)

  return response


  



