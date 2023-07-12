import streamlit as st
import csv
import requests
import io
import random

# Load questions from a CSV file
def load_questions(url):
    questions = []
    response = requests.get(url)
    content = response.content.decode("utf-8")
    reader = csv.reader(io.StringIO(content), delimiter=";")
    for row in reader:
        question = {
            "question": row[0],
            "options": row[1:5],
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
num_questions = st.number_input("Number of questions:", min_value=1, value=5)

# Load the questions from the CSV file
questions = load_questions("https://raw.githubusercontent.com/agoesd/quizPBJ/main/quiz_questions.csv")

# Randomize the order of questions
random.shuffle(questions)

# Initialize the score and user answers
score = 0
user_answers = []

# Display each question and collect the user's answer
for i in range(num_questions):
    st.header(f"Question #{i+1}")
    st.write(questions[i]["question"])
    selected_option = st.selectbox("Select an option:", questions[i]["options"])
    user_answers.append(selected_option)

# Calculate the total score
score = calculate_score(questions[:num_questions], user_answers)

# Display the final score
st.success(f"Total Score: {score}")
