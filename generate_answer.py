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
from langchain_upstage import UpstageEmbeddings
import numpy as np
from transformers import pipeline


load_dotenv()

def cosine_similarity(first_vec, second_vec):
    vec_dot = np.dot(first_vec, second_vec)
    first_norm = np.linalg.norm(first_vec)
    second_norm = np.linalg.norm(second_vec)
    return vec_dot / (first_norm * second_norm)

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


    embedding = UpstageEmbeddings(model="solar-embedding-1-large-query")
    embedded_answer = embedding.embed_query(st.session_state.user_input)
    embedded_definition = embedding.embed_query(st.session_state.word_data["senseinfo"]["definition"]) 
    embed_score = cosine_similarity(embedded_answer, embedded_definition)
    
    sentiment_analysis = pipeline("sentiment-analysis", model="monologg/koelectra-base-finetuned-nsmc")
    sentiment_result = sentiment_analysis(response.content) 
    
    sentiment_score = sentiment_result[0]["score"]
    if sentiment_result[0]["label"] == "negative":
        sentiment_score *= -1

    st.write(embed_score)
    st.write(sentiment_score)
    score = (embed_score + (sentiment_score + 1) / 2) / 2
    
    return((score + 1) / 2 * 100)
