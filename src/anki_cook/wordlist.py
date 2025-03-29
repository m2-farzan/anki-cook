from typing import List

from pydantic import BaseModel


class WordUnannotated(BaseModel):
    original: str
    meaning: str


class WordListUnannotated(BaseModel):
    words: List[WordUnannotated]


class Word(WordUnannotated):
    extra: str


class WordList(BaseModel):
    words: List[Word]
