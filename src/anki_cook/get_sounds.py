from anki_cook.openai_client import openai_client
from typing import List, Mapping, Optional
import os
import re

def get_sounds(language: str, words: List[str], extras: Optional[List[str]] = None) -> Mapping[str, str]:
    sounds = {}
    for word in words:
        word_sanitized = re.sub(r'\W+', '_', word.lower())
        file_path = f"/tmp/anki_cook_{word_sanitized}_{language}.mp3"
        if os.path.exists(file_path):
            print(f"Using cached sound for '{word}' in {language}")
        else:
            print(f"Generating sound for '{word}' in {language}")
            instructions = f"Speak the word '{word}' in {language}."
            if extras:
                extra, *extras = extras
                instructions += f" ({extra})"
            with openai_client().audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice="alloy",
                input=word,
                instructions=instructions,
            ) as response:
                response.stream_to_file(file_path)
        sounds[word] = file_path
    return sounds
