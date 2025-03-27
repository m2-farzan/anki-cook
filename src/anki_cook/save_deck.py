import os
import genanki

def save_deck(deck: genanki.Package, base_title: str) -> None:
    os.makedirs("out", exist_ok=True)
    i = 0
    title = base_title
    while os.path.exists(filename := f"out/{title}.apkg"):
        i += 1
        title = f"{base_title}_{i}"
    deck.write_to_file(filename)
    print(f"Deck saved to {filename}")
