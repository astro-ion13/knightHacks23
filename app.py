'''
Main file for the Streamlit app.

Maverick, Ian, Jay, Richard
10.07.2023


TODO
- Use atlas instead (creative use of MongoDB Atlas)
- Information below
- 3 Columns with information
- Google cloud to generate PDF?
- Information to help the user
- Any cloud computing to help generate PDFs?
- Edit Theme for Morgan Colors

- Chat with our virtual assistant, upload a document for more context

https://www.youtube.com/watch?v=6fs80o7Xm4I&ab_channel=FaniloAndrianasolo

- Uploaded documents
How homeless do I look?
- Recommended Questions

'''

import streamlit as st
import os, tempfile

from langchain.chat_models import ChatOpenAI
from langchain.prompts import *

from langchain import LLMChain

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

import os, tempfile
import streamlit as st
from langchain.llms.openai import OpenAI
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain

from dataclasses import dataclass
from typing import Literal
import streamlit as st

from langchain import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory
import streamlit.components.v1 as components

openai_api_key = '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'



@dataclass
class Message:
    origin: Literal["human", "llm"]
    message: str

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state["history"] = []
    if "conversation" not in st.session_state:
        llm = OpenAI(temperature=0, openai_api_key=openai_api_key, model_name="gpt-3.5-turbo")
        st.session_state.conversation = ConversationChain(llm=llm, memory=ConversationSummaryMemory(llm=llm))


def on_click_callback():
    human_prompt = st.session_state["human_prompt"]
    llm_response = st.session_state.conversation.run(human_prompt)

    st.session_state["history"].append(
        Message("human", human_prompt)
    )
    st.session_state["history"].append(
        Message("llm", llm_response)
    )


def main():
    initialize_session_state()
    
    # Begin the Streamlit App Here
    st.title('MorganAI')


    st.sidebar.title("Upload a File")
    source_doc = st.sidebar.file_uploader("Upload Source Document", type="pdf")

    if not source_doc:
        st.sidebar.error("Please upload a source document.")
        st.error("Please upload a source document to continue.")
    else:
        with st.spinner('Please wait while we analyze your documents...'):
            vectordb = get_vectorstore(source_doc)
            llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

            summary = get_summary(vectordb, llm)
            st.success(summary)
              
    st.write('Hi, I am MorganAI. I am here to help you with your legal needs.')
    chat_palceholder = st.container()
    prompt_placeholder = st.form("Chat-form")

    with chat_palceholder:
        for chat in st.session_state.history:
            st.markdown(f"**MorganAI** - {chat}")

    with prompt_placeholder:
        st.markdown("**Chat** - _Press Enter to submit_")
        cols = st.columns((6, 1))
        cols[0].text_input("Chat", value="Hello", key='human_prompt')
        cols[1].form_submit_button("Send", type="primary", on_click=on_click_callback)
    

def get_vectorstore(source_doc):
    # Save uploaded file temporarily to disk, load and split the file into pages, delete temp file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(source_doc.read())

    loader = PyPDFLoader(tmp_file.name)
    pages = loader.load_and_split()
    os.remove(tmp_file.name)

    # Create embeddings for the pages and insert into Chroma database
    embeddings=OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectordb = Chroma.from_documents(pages, embeddings)

    return vectordb



def get_summary(vectordb: Chroma, llm) -> str:
    '''
    Gets a summary from the vectordb with the current llm
    '''     
    chain = load_summarize_chain(llm, chain_type="stuff")
    search = vectordb.similarity_search(" ")
    summary = chain.run(input_documents=search, question="Write a summary within 200 words.")

    return summary


if __name__ == '__main__':
    main()