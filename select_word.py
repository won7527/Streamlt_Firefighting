import streamlit as st
import json
import os
import random


def select_word():
    if "file_list" not in st.session_state:
        st.session_state.file_list = [file for file in os.listdir("Data") if file.endswith(".json")]
        st.session_state.file_list = sorted(st.session_state.file_list, key=lambda file_name: int(file_name[file_name.find('_') + 1 : file_name.find('.')]))
    question_num = random.randint(0, 1180246)
    file_name = st.session_state.file_list[question_num // 50000]
    file_path = os.path.join("data", file_name)
    st.write(f"랜덤 넘버 : {question_num}")
    st.write(file_name)
    with open(file_path, 'r', encoding="utf-8") as file:
        file_data = json.load(file)
        word_data = file_data["channel"]["item"]
    st.write(word_data[question_num  - 50000 * (question_num // 50000)])
    return(word_data[question_num  - 50000 * (question_num // 50000)])

# for filename in file_list:
#     if filename.endswith('.json'):
#         filepath = os.path.join(file_dir_path, filename) 
#         with open(filepath, 'r', encoding='utf-8') as file: 
#             json_data = json.load(file)
#             for temp_data in json_data["channel"]["item"]:
#                 data.append(temp_data)
            # data.append(json_data["channel"]["item"])
#st.write(len(data))
#print(data)