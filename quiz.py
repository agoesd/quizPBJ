import streamlit as st
import pandas as pd
import random
from streamlit import caching

# Load questions from a CSV file
def load_questions(url):
    df = pd.read_csv(url, delimiter=";")
    questions = []
    for _, row in df.iterrows():
        options = [row[i] for i in range(1, 5)]
        question = {
            "question": row[0],
            "options": options,
            "answer": row[5]
        }
        questions.append(question)
    return questions

# Randomize the order of questions and options
def randomize_questions(questions):
    random.shuffle(questions)
    for question in questions:
        random.shuffle(question["options"])
    return questions

# Calculate the total score
def calculate_score(questions, user_answers):
    score = 0
    for i in range(len(questions)):
        if user_answers[i] == questions[i]["answer"]:
            score += 4
    return score

# Create a SessionState class
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Create a Streamlit app
st.title("Quiz Time!")

# Load the questions from the CSV file and randomize the options
questions = load_questions("https://raw.githubusercontent.com/agoesd/quizPBJ/main/quiz_questions.csv")
questions = randomize_questions(questions)

# Maximum number of questions
max_num_questions = len(questions)

# Get the number of questions to load from the user
num_questions = st.number_input("Number of questions:", min_value=1, max_value=max_num_questions, value=5, key="num_questions")

submitted_num_questions = st.button("Submit Number of Questions")

if submitted_num_questions:
    selected_questions = questions[:num_questions]
    session_state = SessionState(selected_questions=selected_questions, quiz_started=True, question_index=0, user_answers=[None] * num_questions)
    caching.clear_cache()
else:
    session_state = SessionState()

if session_state.quiz_started:
    question = session_state.selected_questions[session_state.question_index]
    st.header(f"Question #{session_state.question_index + 1}")
    st.write(question["question"])
    selected_option = st.selectbox(f"Select an option for Question #{session_state.question_index + 1}:", question["options"], key=f"options_{session_state.question_index}")
    session_state.user_answers[session_state.question_index] = selected_option

    session_state.question_index += 1
    if session_state.question_index < num_questions:
        question = session_state.selected_questions[session_state.question_index]
        st.header(f"Question #{session_state.question_index + 1}")
        st.write(question["question"])

    if session_state.question_index == num_questions:
        submitted = st.button("Submit")
        if submitted:
            # Calculate the total score
            score = calculate_score(session_state.selected_questions, session_state.user_answers)

            # Display the final score
            st.success(f"Total Score: {score}")
