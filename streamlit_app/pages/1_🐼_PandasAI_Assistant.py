import streamlit as st
import pandas as pd
from pandasai import Agent
import matplotlib.pyplot as plt
import os
from langchain_community.llms import Ollama

st.session_state.field_descriptions = "field_descriptions.json"
st.session_state.llm = Ollama(model="llama3.1", temperature=0)
st.session_state.temporary_file_path = "REPLACE WITH PATH TO THE TEMPORARY IMAGE FILE"

st.set_page_config(page_title="PandasAI Assistant", page_icon="🐼")
st.markdown("# PandasAI Assistant")
st.session_state.df = None

if st.session_state.df is None:
    file_path = f'prompt-data/prompt_history.txt'
    open(file_path, 'a').close()

    uploaded_file = st.file_uploader(
        "Choose a CSV file.",
        type="csv",
    )
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df

if st.session_state.df is not None:

    # Create an instance of the PandasAI Agent
    agent = Agent(st.session_state.df , config={
            "llm": st.session_state.llm,
            "verbose": True,
            "conversational": True,
            "field_descriptions": st.session_state.field_descriptions,
            "enable_cache": True
        })
    
    # Streamlit application
    st.title('PandasAI Assistant')

    with st.form("Question"):
        question = st.text_input("Question", value="", type="default")
        submitted = st.form_submit_button("Submit")
        if submitted:
            with st.spinner():
                response = agent.chat(question)
                
                if os.path.isfile(st.session_state.temporary_file_path):
                    dir_path = os.path.dirname(os.path.realpath(__file__))
                    im = plt.imread(st.session_state.temporary_file_path)
                    st.image(im)
                    os.remove(st.session_state.temporary_file_path )

                    with open(file_path, "a") as myfile:
                        myfile.write(f"Question: {question} \n Answer: An image was provided as a response. To see the image open the prompt-data/images folder.\n\n")
                
                elif response is not None:
                    st.write(response)
                    with open(file_path, "a") as myfile:
                        myfile.write(f"Question: {question} \n Answer: {response}\n\n")
            
    st.subheader("Current dataframe:")
    st.write(st.session_state.df)
    f = open(file_path, "r")
    st.subheader("Prompt history:")
    st.write(f.read())

    if st.button("Clear"):
        st.session_state.df = None
        os.remove(file_path)
