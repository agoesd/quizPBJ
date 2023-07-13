import streamlit as st
import pandas as pd
import random

# Load questions from a CSV file
def load_questions(url):
    df = pd.read_csv(url, delimiter=";")
    questions = []
    for _, row in df.iterrows():
        options = [row[i] for i in range(1, 5)]
        question = {
            "question": row[0],
            "options": options,
            "answer": row[5]  # Assuming the answer is in column 6
        }
        questions.append(question)
    return questions

# Randomize the order of options for a question
def randomize_options(question):
    options = question["options"]
    random.shuffle(options)
    question["options"] = options
    return question

# Create a Streamlit app
st.title("Quiz Time!")

# Load the questions from the CSV file
questions = load_questions("https://raw.githubusercontent.com/agoesd/quizPBJ/main/quiz_questions.csv")

# Maximum number of questions
max_num_questions = len(questions)

# Get the number of questions to load from the user
num_questions = st.number_input("Number of questions:", min_value=1, max_value=max_num_questions, value=5, key="num_questions")

submitted_num_questions = st.button("Submit Number of Questions")

if submitted_num_questions:
    selected_questions = random.sample(questions, num_questions)
    st.session_state["selected_questions"] = selected_questions
    st.session_state["quiz_started"] = True
    st.session_state["question_index"] = 0
    st.session_state["user_answers"] = [None] * num_questions
    st.session_state["score"] = 0

if st.session_state.get("quiz_started"):
    question = st.session_state["selected_questions"][st.session_state["question_index"]]
    question = randomize_options(question)
    st.header(f"Question #{st.session_state['question_index'] + 1}")
    st.write(question["question"])
    selected_option = st.radio(f"Select an option for Question #{st.session_state['question_index'] + 1}:", question["options"], key=f"options_{st.session_state['question_index']}")
    st.session_state["user_answers"][st.session_state["question_index"]] = selected_option

    if st.button("Next Question"):
        st.session_state["question_index"] += 1

if not st.session_state.get("quiz_started"):
    st.write("Quiz ended. Here's your score:")
    score = sum(
        4 if answer == question["answer"] else 0
        for answer, question in zip(st.session_state["user_answers"], st.session_state["selected_questions"])
    )
    st.success(f"Total Score: {score}")
