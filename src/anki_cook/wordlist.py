from pydantic import BaseModel
from typing import List


class Word(BaseModel):
    original: str
    meaning: str
    extra: str


class WordList(BaseModel):
    words: List[Word]
