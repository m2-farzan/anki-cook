from argparse import ArgumentParser
from anki_cook.gen_wordlist import gen_wordlist
from anki_cook.utils.source_envfile import source_envfile
from anki_cook.make_deck import make_deck
from anki_cook.save_deck import save_deck
from anki_cook.get_sounds import get_sounds
import re


def main():
    source_envfile()
    args = parse_args()
    deck = gen_wordlist(args.topic, args.native, args.target, args.extra, args.count)
    for word in deck.words:
        print(f"{word.original}: {word.meaning} ({word.extra})")
    title = re.sub(r"\W+", "_", args.topic.lower())
    target_sounds = args.target_tts and get_sounds(
        args.target,
        [word.original for word in deck.words],
        [word.extra for word in deck.words],
    )
    native_sounds = args.native_tts and get_sounds(
        args.native, [word.meaning for word in deck.words]
    )
    package = make_deck(deck, title, target_sounds, native_sounds)
    save_deck(package, title)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("topic", help="Topic to generate a deck for")
    parser.add_argument(
        "--native",
        help="Native language for the deck. Use plain English name, e.g. 'English'",
    )
    parser.add_argument(
        "--target",
        help="Target language for the deck. Use plain English name, e.g. 'Spanish'",
    )
    parser.add_argument(
        "--extra",
        help="Extra information to include in the target side, e.g. Hiraganas for Japanese. Use plain English name, e.g. 'Hiragana'",
        default="",
    )
    parser.add_argument(
        "--count", help="Number of words to include in the deck", type=int, default=30
    )
    parser.add_argument(
        "--target-tts",
        help="Include sound for the target language",
        action="store_true",
    )
    parser.add_argument(
        "--native-tts",
        help="Include sound for the native language",
        action="store_true",
    )
    return parser.parse_args()
