import os
import streamlit as st
import pandas as pd
from src.generator.question_generator import QuestionGenerator

def rerun():
    st.session_state["rerun"] = not st.session_state.get("rerun", False)

class QuizManager:
    def __init__(self):
        self.questions = []
        self.userResponses = []
        self.score = []
        self.generator = QuestionGenerator()

    def create_quiz(self, topic: str, difficulty: str, num_questions: int, question_type: str) -> pd.DataFrame:
        self.questions = []
        self.userResponses = []
        self.score = []

        for _ in range(num_questions):
            try:
                if question_type == "MCQ":
                    mcq = self.generator.generate_mcq(topic, difficulty.lower())
                    self.questions.append(
                        {
                            "type": "MCQ",
                            "question": mcq.question,
                            "options": mcq.options,
                            "answer": mcq.answer
                        }
                    )
                else:
                    fill_blank = self.generator.generate_fill_in_the_blank(topic, difficulty.lower())
                    self.questions.append({
                        "type": "Fill in the Blank",
                        "question": fill_blank.question,
                        "answer": fill_blank.answer
                    })
            except Exception as e:
                st.error(f"Error generating question: {e}")
                continue
        
        return True
    
    def attempt_quiz(self):
        for idx, q in enumerate(self.questions):
            st.write(f"Question {idx + 1}: {q['question']}")
            if q["type"] == "MCQ":
                options = q["options"]
                user_answer = st.radio("Select an option:", options, key=f"mcq_{idx}")
                self.userResponses.append(user_answer)
            else:
                user_answer = st.text_input("Your answer:", key=f"fill_blank_{idx}")
                self.userResponses.append(user_answer)
        
        return True
    

    def get_results(self):
        self.score = []
        for idx, q in enumerate(self.questions):
            result_dict = {
                "question": q["question"],
                "correct_answer": q["answer"],
                "user_answer": self.userResponses[idx],
                "is_correct": False
            }
            if q["type"] == "MCQ":
                result_dict["is_correct"] = (result_dict["user_answer"] == result_dict["correct_answer"])
            else:
                result_dict["is_correct"] = (result_dict["user_answer"].strip().lower() == result_dict["correct_answer"].strip().lower())
            self.score.append(result_dict)
        return True

    def dataframe_results(self) -> pd.DataFrame:
        if not self.score:
            return pd.DataFrame()
        
        return pd.DataFrame(self.score)
    
    def save_results(self):
        df = self.dataframe_results()
        filename = f"quiz_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        