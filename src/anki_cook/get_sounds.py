import logging
import os
import re
from typing import List, Mapping, Optional

from anki_cook.openai_client import openai_client


def get_sounds(
    language: str,
    words: List[str],
    extras: Optional[List[str]] = None,
    feedback_cb=None,
) -> Mapping[str, str]:
    sounds = {}
    for i, word in enumerate(words):
        if feedback_cb:
            feedback_cb(f"Generating {language} sound ({i + 1}/{len(words)})")
        word_sanitized = re.sub(r"\W+", "_", word.lower())
        file_path = f"/tmp/anki_cook_{word_sanitized}_{language}.mp3"
        if os.path.exists(file_path):
            logging.info(f"Using cached sound for '{word}' in {language}")
        else:
            logging.info(f"Generating sound for '{word}' in {language}")
            instructions = f"Say the word '{word}' in {language}."
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
