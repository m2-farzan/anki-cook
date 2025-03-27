## Purpose

Generate anki cards about any topic!

I never forget the words that I use in real life so I try to use this method before I go to an event, etc.

## Installation

```
poetry install
```

Also copy `.env.example` to `.env` and update the value. You should be able to use open-ai's free tier.

## Usage:

The structure is as follows but all arguments accept natural language input:

```
$ poetry run anki_cook --native english --target japanese_kana --extra japanese_kanji cooking
```

This command generates an `.apkg` file and also prints the following preview:
```
りょうり: Cooking (料理)
あぶら: Oil (油)
さとう: Sugar (砂糖)
しお: Salt (塩)
にく: Meat (肉)
さかな: Fish (魚)
やさい: Vegetables (野菜)
くだもの: Fruits (果物)
こむぎこ: Flour (小麦粉)
たまご: Egg (卵)
ごはん: Rice (ご飯)
やく: To grill (焼く)
あげる: To fry (揚げる)
にる: To boil (煮る)
うでる: To cook in water (茹でる)
むす: To steam (蒸す)
まぜる: To mix (混ぜる)
きる: To cut (切る)
むく: To peel (剥く)
しんぶん: Ingredient (成分)
なべ: Pot (鍋)
まないた: Cutting board (まな板)
ほうちょう: Kitchen knife (包丁)
おたま: Ladle (お玉)
しゃもじ: Rice scoop (杓文字)
フライパン: Frying pan (フライパン)
れいとう: Freezing (冷凍)
じゅんび: Preparation (準備)
あじみ: Tasting (味見)
つける: To serve (漬ける)
Deck saved to out/cooking_1.apkg
```

# Improvement ideas

- [ ] Simple flask front-end for easy use!
- [ ] More QA and tuning
- [ ] Better card ordering (some shuffle?)

# More examples

To get an idea, see `Examples.md`.
