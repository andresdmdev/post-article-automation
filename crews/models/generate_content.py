from pydantic import BaseModel

class Generate_Content(BaseModel):
    topic: str
    year: int
    month: int
    day: int
    result_content: str