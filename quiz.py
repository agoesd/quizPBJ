import streamlit as st
import pandas as pd
import random
from streamlit_secrets import SessionState

# Load questions from a CSV file
def load_questions(url):
    df = pd.read_csv(url, delimiter=";")
    questions = []
    for _, row in df.iterrows():
        question = {
            "question": row[0],
            "options": [row[i] for i in range(1, 5)],
            "answer": row[5]
        }
        questions.append(question)
    return questions

# Calculate the total score
def calculate_score(questions, user_answers):
    score = 0
    for i in range(len(questions)):
        if user_answers[i] == questions[i]["answer"]:
            score += 4
    return score

# Create a Streamlit app
st.title("Quiz Time!")

# Get the number of questions to load from the user
session_state = SessionState.get(num_questions=5, quiz_started=False, random_order=[])

num_questions = st.number_input("Number of questions:", min_value=1, value=session_state.num_questions, key="num_questions")

if st.button("Start Quiz"):
    session_state.random_order = list(range(num_questions))
    random.shuffle(session_state.random_order)
    session_state.quiz_started = True

if session_state.quiz_started:
    # Load the questions from the CSV file
    questions = load_questions("quiz_questions.csv")

    # Initialize the score and user answers
    score = 0
    user_answers = []

    # Display each question and collect the user's answer
    for i in range(session_state.num_questions):
        question_index = session_state.random_order[i]
        st.header(f"Question #{i+1}")
        st.write(questions[question_index]["question"])
        selected_option = st.selectbox(f"Select an option for Question #{i+1}:", questions[question_index]["options"])
        user_answers.append(selected_option)

    # Submit answers and calculate the total score
    submitted = st.button("Submit")
    if submitted:
        # Calculate the total score
        score = calculate_score([questions[idx] for idx in session_state.random_order[:session_state.num_questions]], user_answers)
        
        # Display the final score
        st.success(f"Total Score: {score}")
