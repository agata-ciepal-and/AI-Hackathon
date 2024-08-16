import streamlit as st
from langchain.llms import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate

# Set up the Langchain components

# Define the LLM using Langchain's Ollama integration (replace with your own config if needed)
ollama_llm = Ollama(model="llama3.1", temperature=0)  # Modify this if your API URL is different

# Create a conversation memory to store chat history
memory = ConversationBufferMemory()

# Define the conversation chain
conversation_chain = ConversationChain(llm=ollama_llm, memory=memory)

# Streamlit App UI
st.title("Chatbot v2")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get user input
user_input = st.text_input("You:", key="input")

if user_input:
    # Add the user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Use Langchain to get the response from Ollama
    response = conversation_chain.run(input=user_input)
    
    # Add the LLM response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display the conversation
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.write(msg["content"], is_user=True)
    else:
        st.write(msg["content"])