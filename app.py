import os
from src.utils.helper import *
import streamlit as st
from dotenv import load_dotenv
from src.generator.question_generator import QuestionGenerator
load_dotenv()

class QuizApp:
    def __init__(self):
        if "quiz_manager" not in st.session_state:
            st.session_state.quiz_manager = QuizManager()

    def run(self):
        st.title("Study Buddy Quiz Generator")
        question_type = st.selectbox("Select question type:", ["MCQ", "Fill in the Blank"])
        topic = st.text_input("Enter a topic for the quiz:")
        difficulty = st.selectbox("Select difficulty level:", ["Easy", "Medium", "Hard"])
        num_questions = st.slider("Number of questions:", 1, 10, 5)
        
        quiz_manager = st.session_state.quiz_manager

        if st.button("Generate Quiz"):
            if topic:
                with st.spinner("Generating quiz..."):
                    success = quiz_manager.create_quiz(topic, difficulty, num_questions, question_type)
                    if success:
                        st.success("Quiz generated successfully! Attempt the quiz below.")
            else:
                st.error("Please enter a topic to generate the quiz.")

        if quiz_manager.questions:
            quiz_manager.attempt_quiz()
            if st.button("Get Results"):
                quiz_manager.get_results()
                st.dataframe(quiz_manager.dataframe_results())
                st.markdown("score" + " : " + str(len([s for s in quiz_manager.score if s['is_correct']])) + "/" + str(len(quiz_manager.questions)) + " (" + str(len([s for s in quiz_manager.score if s['is_correct']]) / len(quiz_manager.questions) * 100) + "%)")

        
if __name__ == "__main__":
    app = QuizApp()
    app.run()