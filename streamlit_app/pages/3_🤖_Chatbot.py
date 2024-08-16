import streamlit as st
from openai import OpenAI
import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
)

llm = Ollama(model="llama3.1", temperature=0)

st.write("# Chatbot")


# Define a prompt template for the chatbot
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please response to the questions"),
        ("user","Question:{question}")
    ]
)

input_text=st.text_input("Ask your question!")  # Create a text input field in the Streamlit app

# Create a chain that combines the prompt and the Ollama model
chain=prompt|llm

# Invoke the chain with the input text and display the output
if input_text:
    st.write(chain.invoke({"question":input_text}))