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
    selected_questions = random.sample(questions, num_questions)
    st.session_state["selected_questions"] = selected_questions
    st.session_state["quiz_started"] = True
    st.session_state["question_index"] = 0
    st.session_state["user_answers"] = [None] * num_questions

if st.session_state.get("quiz_started"):
    question = st.session_state["selected_questions"][st.session_state["question_index"]]
    st.header(f"Question #{st.session_state['question_index'] + 1}")
    st.write(question["question"])
    selected_option = st.selectbox(f"Select an option for Question #{st.session_state['question_index'] + 1}:", question["options"], key=f"options_{st.session_state['question_index']}")
    st.session_state["user_answers"][st.session_state["question_index"]] = selected_option

    if st.session_state["question_index"] < num_questions - 1:
        st.button("Next Question", key="next_question")
    else:
        submitted = st.button("Submit")

    if "next_question" in st.session_state:
        st.session_state["question_index"] += 1
        del st.session_state["next_question"]

if submitted:
    # Calculate the total score
    score = calculate_score(st.session_state["selected_questions"], st.session_state["user_answers"])
    
    # Display the final score
    st.success(f"Total Score: {score}")
