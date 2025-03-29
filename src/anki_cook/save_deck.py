import logging
import os
from typing import Optional

import genanki


def save_deck(
    deck: genanki.Package, base_title: str, base_path: Optional[str] = None
) -> None:
    if not base_path:
        base_path = "out"
    os.makedirs(base_path, exist_ok=True)
    i = 0
    title = base_title
    while os.path.exists(filename := f"{base_path}/{title}.apkg"):
        i += 1
        title = f"{base_title}_{i}"
    deck.write_to_file(filename)
    logging.info(f"Deck saved to {filename}")
    return filename
