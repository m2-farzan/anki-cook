import os
import re

from anki_cook.openai_client import openai_client
from anki_cook.wordlist import WordList


def gen_wordlist(
    topic, native_language, target_language, extra_field, count
) -> WordList:
    cache_key = f"{topic}-{native_language}-{target_language}-{extra_field}-{count}"
    cache_key = re.sub(r"\W+", "_", cache_key)
    cache_file = f"/tmp/anki_cook_{cache_key}.json"
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            print(f"Loading wordlist from cache: {cache_file}")
            return WordList.model_validate_json(f.read())
    result = _gen_wordlist_uncached(
        topic, native_language, target_language, extra_field, count
    )
    with open(cache_file, "w") as f:
        f.write(result.model_dump_json())
    return result


def _gen_wordlist_uncached(
    topic, native_language, target_language, extra_field, count
) -> WordList:
    prompt = f"Generate a wordlist of size {count} for the topic '{topic}' in {target_language} with meanings in {native_language}."
    if extra_field:
        prompt += f" Include {extra_field} in the extra field."
    wordlist = openai_client().beta.chat.completions.parse(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format=WordList,
    )
    return wordlist.choices[0].message.parsed
