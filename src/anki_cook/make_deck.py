from os.path import basename
from typing import Mapping, Optional

import genanki

from anki_cook.utils.load_static import load_style, load_template
from anki_cook.wordlist import WordList


def make_deck(
    word_list: WordList,
    title: str,
    target_sounds: Optional[Mapping[str, str]],
    native_sounds: Optional[Mapping[str, str]],
) -> genanki.Package:
    front_t = load_template("front")
    native_t = load_template("native")
    target_t = load_template("target")

    anki_model = genanki.Model(
        1607592013,
        "Simple Model",
        fields=[
            {"name": "target_word"},
            {"name": "target_extra"},
            {"name": "target_sound"},
            {"name": "native_word"},
            {"name": "native_sound"},
            {"name": "sort_id"},
        ],
        templates=[
            {
                "name": "target -> native",
                "qfmt": target_t,
                "afmt": front_t + native_t,
            },
            {
                "name": "native -> target",
                "qfmt": native_t,
                "afmt": front_t + target_t,
            },
        ],
        css=load_style(),
    )

    anki_deck = genanki.Deck(2059404118, title)
    sound_list = []
    for i, word in enumerate(word_list.words):
        target_word = word.original
        target_extra = word.extra
        if target_sounds and (s := target_sounds.get(word.original)):
            target_sound = f"[sound:{basename(s)}]"
            sound_list.append(s)
        else:
            target_sound = ""
        native_word = word.meaning
        if native_sounds and (s := native_sounds.get(word.meaning)):
            native_sound = f"[sound:{basename(s)}]"
            sound_list.append(s)
        else:
            native_sound = ""
        sort_id = str(i)
        anki_note = genanki.Note(
            model=anki_model,
            fields=[
                target_word,
                target_extra,
                target_sound,
                native_word,
                native_sound,
                sort_id,
            ],
        )
        anki_deck.add_note(anki_note)

    package = genanki.Package(anki_deck)
    package.media_files = sound_list

    return package
