import streamlit as st
import pandas as pd
import random

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
        if user_answers[i] == questions[i]["answer"] or user_answers[i] == questions[i]["options"][int(questions[i]["answer"][-1]) - 1]:
            score += 4
    return score

# Create a Streamlit app
st.title("Quiz Time!")

# Load the questions from the CSV file
questions = load_questions("quiz_questions.csv")

# Maximum number of questions
max_num_questions = len(questions)

# Get the number of questions to load from the user
num_questions = st.number_input("Number of questions:", min_value=1, max_value=max_num_questions, value=5, key="num_questions")

submitted_num_questions = st.button("Submit Number of Questions")

if submitted_num_questions:
    random_order = list(range(num_questions))
    random.shuffle(random_order)
    st.session_state["random_order"] = random_order
    st.session_state["quiz_started"] = True

if st.session_state.get("quiz_started"):
    # Display each question and collect the user's answer
    user_answers = []
    for i in range(num_questions):
        question_index = st.session_state["random_order"][i]
        st.header(f"Question #{i+1}")
        st.write(questions[question_index]["question"])
        selected_option = st.selectbox(f"Select an option for Question #{i+1}:", questions[question_index]["options"])
        user_answers.append(selected_option)

    # Submit answers and calculate the total score
    submitted = st.button("Submit")
    if submitted:
        # Calculate the total score
        score = calculate_score([questions[idx] for idx in st.session_state["random_order"][:num_questions]], user_answers)
        
        # Display the final score
        st.success(f"Total Score: {score}")
