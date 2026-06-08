from langchain_core.output_parsers import PydanticOutputParser
from src.prompts.template import mcq_prompt_template, fill_blank_prompt_template
from src.models.question_schemas import MCQQuestion, FillInTheBlankQuestion
from src.llm.groq_client import get_groq_client
from src.config.settings import settings
from src.common.custom_exception import CustomException
from src.common.logger import get_logger

class QuestionGenerator:
    def __init__(self):
        self.llm = get_groq_client()
        self.logger = get_logger(__name__)

    def generate_mcq(self,topic: str, difficulty: str) -> MCQQuestion:
        try:
            prompt = mcq_prompt_template.format(topic=topic, difficulty=difficulty)
            output_parser = PydanticOutputParser(pydantic_object=MCQQuestion)
            response = self.llm.invoke(prompt)
            question = output_parser.parse(response.content)
            return question
        except Exception as e:
            self.logger.error(f"Error generating MCQ: {e}")
            raise CustomException("Failed to generate multiple-choice question", e)
    
    def generate_fill_in_the_blank(self, topic: str, difficulty: str) -> FillInTheBlankQuestion:
        try:
            prompt = fill_blank_prompt_template.format(topic=topic, difficulty=difficulty)
            output_parser = PydanticOutputParser(pydantic_object=FillInTheBlankQuestion)
            response = self.llm.invoke(prompt)
            question = output_parser.parse(response.content)
            return question
        except Exception as e:
            self.logger.error(f"Error generating fill-in-the-blank question: {e}")
            raise CustomException("Failed to generate fill-in-the-blank question", e)
        
if __name__ == "__main__":
    generator = QuestionGenerator()
    mcq = generator.generate_mcq(topic="Geography", difficulty="easy")
    print(mcq)
    fill_blank = generator.generate_fill_in_the_blank(topic="IPL2026", difficulty="medium")
    print(fill_blank)