from typing import List

from pydantic import BaseModel


class Word(BaseModel):
    original: str
    meaning: str
    extra: str


class WordList(BaseModel):
    words: List[Word]
