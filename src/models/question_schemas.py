from typing import List
from pydantic import BaseModel, Field, validator

class MCQQuestion(BaseModel):
    question: str = Field(description="A clear, specific multiple-choice question.")

    options: List[str] = Field(description="An array of exactly 4 possible answers.")

    answer: str = Field(description="The correct answer, which must be one of the options.")

    @validator('question')
    def question_must_not_be_empty(cls, v):
        if isinstance(v,dict):
            return v.get("description", str(v))
        return str(v)
    
class FillInTheBlankQuestion(BaseModel):
    question: str = Field(description="A sentence with '_____' marking where the blank should be.")

    answer: str = Field(description="The correct word or phrase that belongs in the blank.")

    @validator('question')
    def question_must_not_be_empty(cls, v):
        if isinstance(v,dict):
            return v.get("description", str(v))
        return str(v)