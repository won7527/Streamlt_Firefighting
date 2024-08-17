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

load_dotenv()
def generate_answer():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "store" not in st.session_state:
        st.session_state["store"] = dict()

    with open("Prompts/answer.prompt", "r", encoding="utf-8") as file:
        prompt = file.read().strip()
    system_prompt = prompt
    custom_prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template("{answer}, {definition}")
        ]
    )
    llm = ChatOpenAI(name="gpt-4o-mini")
    chain = custom_prompt | llm
    response = chain.invoke({"answer" : st.session_state.user_input,
                             "definition" : st.session_state.word_data["senseinfo"]["definition"]})
    
    st.session_state["messages"].append(ChatMessage(role="user", content=st.session_state.user_input))
    st.session_state["messages"].append(ChatMessage(role="assistant", content=response.content))
    st.write(st.session_state.user_input)
    return(st.session_state["messages"][-1].content)
