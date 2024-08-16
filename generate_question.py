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
    session_id = 112
    def get_session_history(session_id):
        if session_id not in st.session_state["store"]:
            st.session_state["store"][session_id] = ChatMessageHistory()
        return st.session_state["store"][session_id]
        
    word_data = select_word.select_word()

    with open("Prompts/question.prompt", "r", encoding="utf-8") as file:
        prompt = file.read().strip()
    system_prompt = prompt
    custom_prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(system_prompt),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{word}, {definition}")
        ]
    )
   
    llm = ChatOpenAI(name="gpt-4o-mini")
    chain = custom_prompt | llm
    chain_with_runnable = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="word",
        history_messages_key="history",
    )
    response = chain_with_runnable.invoke({
        "word" : word_data["wordinfo"]["word"],
        "definition": word_data["senseinfo"]["definition"],
    }, config={"configurable": {"session_id": session_id}})
    st.session_state["messages"].append(ChatMessage(role="assistant", content=response.content))
    return(st.session_state["messages"][-1].content)
#st.write(st.session_state["messages"][0].content)
