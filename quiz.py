import streamlit as st
import pandas as pd
import random

# Load questions from a CSV file and randomize the options
def load_questions(url):
    df = pd.read_csv(url, delimiter=";")
    questions = []
    for _, row in df.iterrows():
        options = [row[i] for i in range(1, 5)]
        random.shuffle(options)
        answer_index = int(row[5][-1]) - 1
        question = {
            "question": row[0],
            "options": options,
            "answer_index": answer_index,
            "answer": options[answer_index]
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

# Load the questions from the CSV file and randomize the options
questions = load_questions("quiz_questions.csv")

# Maximum number of questions
max_num_questions = len(questions)

# Get the number of questions to load from the user
num_questions = st.number_input("Number of questions:", min_value=1, max_value=max_num_questions, value=5, key="num_questions")

submitted_num_questions = st.button("Submit Number of Questions")

if submitted_num_questions:
    random_order = random.sample(range(max_num_questions), num_questions)
    st.session_state["random_order"] = random_order
    st.session_state["quiz_started"] = True

if st.session_state.get("quiz_started"):
    # Display each question and collect the user's answer
    user_answers = st.session_state.get("user_answers", [])
    for i, question_index in enumerate(st.session_state["random_order"]):
        question = questions[question_index]
        st.header(f"Question #{i+1}")
        st.write(question["question"])
        options = question["options"]
        selected_option = st.selectbox(f"Select an option for Question #{i+1}:", options, key=f"question_{i}")
        if len(user_answers) < num_questions:
            user_answers.append(selected_option)
        else:
            user_answers[i] = selected_option
    st.session_state["user_answers"] = user_answers

    # Submit answers and calculate the total score
    submitted = st.button("Submit")
    if submitted:
        # Calculate the total score
        score = calculate_score([questions[idx] for idx in st.session_state["random_order"]], user_answers)
        
        # Display the final score
        st.success(f"Total Score: {score}")
