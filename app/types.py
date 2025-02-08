from pydantic import BaseModel, Field
from typing import List


class FilterInput(BaseModel):
    text: str = Field(description="text to be filtered for sensitive words")
    replace_char: str = Field(description="symbols used to replace sensitive words", default="*")


class FilterOutput(BaseModel):
    is_sensitive: bool = Field(description="whether sensitive words are detected")
    filtered: str = Field(description="filtered text")
    dirty_words: List[str] = Field(description="sensitive words detected")
