from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.messages import ChatMessage 
from dotenv import load_dotenv
import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
import select_word

load_dotenv()
def generate_question():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "store" not in st.session_state:
        st.session_state["store"] = dict()
    if "word_data" not in st.session_state:
        st.session_state.word_data = ""
    st.session_state.word_data = select_word.select_word()

    with open("Prompts/question.prompt", "r", encoding="utf-8") as file:
        prompt = file.read().strip()
    system_prompt = prompt
    custom_prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template("{word}, {definition}")
        ]
    )
   
    llm = ChatOpenAI(name="gpt-4o-mini")
    chain = custom_prompt | llm
    response = chain.invoke({"word" : st.session_state.word_data["wordinfo"]["word"],
                             "definition": st.session_state.word_data["senseinfo"]["definition"]})

    st.session_state["messages"].append(ChatMessage(role="assistant", content=response.content))
    return(st.session_state["messages"][-1].content)

def generate_question_provoke():

    st.session_state.word_data = select_word.select_word()
    with open("Prompts/question_provoke.prompt", "r", encoding="utf-8") as file:
        prompt = file.read().strip()
    system_prompt = prompt
    custom_prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template("{word}, {definition}")
        ]
    )
   
    llm = ChatOpenAI(name="gpt-4o-mini")
    chain = custom_prompt | llm
    response = chain.invoke({"word" : st.session_state.word_data["wordinfo"]["word"],
                             "definition": st.session_state.word_data["senseinfo"]["definition"]})

    st.session_state["messages"].append(ChatMessage(role="assistant", content=response.content))
    return(st.session_state["messages"][-1].content)
