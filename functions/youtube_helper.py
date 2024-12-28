from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import YoutubeLoader
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import time
import streamlit as st
from dotenv import load_dotenv
import os

def add_transcipt_to_db(video_url: str):
  embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    openai_api_key=os.environ.get("OPENAI_API_KEY")
  )

  pc = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))
  index_name = "youtube-assistant"
  index = pc.Index(index_name)
  vector_store = PineconeVectorStore(embedding=embeddings, index=index)

  loader = YoutubeLoader.from_youtube_url(video_url)
  transcript = loader.load()

  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=1000, 
      chunk_overlap=200,
      add_start_index=True)
  
  all_splits = text_splitter.split_documents(transcript)
  _ = vector_store.add_documents(documents=all_splits)

  return vector_store

def get_response_from_query(vector_store, query, k=4):
  retrieved_docs = vector_store.similarity_search(query, k=k)
  retrieved_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

  llm = ChatOpenAI(model="gpt-4o-mini")

  prompt = PromptTemplate(
    input_variables=['question, context'],
    template="""
    You are an assistant that answers questions about Youtube videos based on the video's transcript.

    Answer this question: {question}

    Use this segment of the video's transcript: {context}

    If you do not have enough information to answer the question, reply with "I don't have enough information to answer your question.".
    """
  )

  message = prompt.invoke({
    'question': query,
    'context': retrieved_content})
  
  response = llm.invoke(message)

  return response


  



