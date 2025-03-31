import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor
from os.path import basename

import pydantic
from flask import (Flask, Response, make_response, render_template, request,
                   send_from_directory)

import anki_cook.server.schema as schema
from anki_cook.gen_wordlist import gen_wordlist
from anki_cook.get_sounds import get_sounds
from anki_cook.make_deck import make_deck
from anki_cook.save_deck import save_deck
from anki_cook.utils.source_envfile import source_envfile

source_envfile()
app = Flask(__name__)
word_list_store = {}
deck_store = {}
executor = ThreadPoolExecutor(max_workers=4)
logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] %(message)s", level=logging.INFO
)


class JSONResponse(Response):
    default_mimetype = "application/json"


@app.route("/")
def index():
    try:
        d = schema.GenerateWordListSchema(**request.args)
    except pydantic.ValidationError as e:
        d = None
    return render_template("index.html", d=d)


@app.route("/css/<path:path>")
def send_css(path):
    return send_from_directory("css", path)


@app.route("/scripts/<path:path>")
def send_scripts(path):
    return send_from_directory("scripts", path)


@app.route("/images/<path:path>")
def send_img(path):
    return send_from_directory("images", path)


@app.route("/fonts/<path:path>")
def send_font(path):
    return send_from_directory("fonts", path)


@app.route("/favicon.ico")
def send_icon():
    return send_from_directory("images", "favicon.ico")


@app.route("/about")
def about():
    return render_template("about.html")


@app.post("/api/generate/preview")
def generate_preview():
    try:
        d = schema.GenerateWordListSchema(**request.json)
    except pydantic.ValidationError as e:
        return Response(status=422, response=str(e))
    if d not in word_list_store:
        word_list_store[d] = None
        executor.submit(_generate_preview, d)
        time.sleep(0.1)  # trick to make cached requests short-circuit poll
    if word_list_store[d] is None:
        return Response(status=202, response="{}")
    return Response(
        status=200,
        response="{}",
        headers={
            "Location": f"/preview?topic={d.topic}&native={d.native}&target={d.target}&extra={d.extra}&count={d.count}"
        },
    )


def _generate_preview(d: schema.GenerateWordListSchema):
    t_start = time.perf_counter()
    logging.info(
        f"Generating preview for [{d.topic}, {d.native}, {d.target}, {d.extra}, {d.count}]"
    )
    deck = gen_wordlist(d.topic, d.native, d.target, d.extra, d.count)
    word_list_store[d] = deck
    t_end = time.perf_counter()
    logging.info(f"Preview generated in {t_end - t_start:.2f}s")


@app.route("/preview")
def preview():
    try:
        d = schema.GenerateWordListSchema(**request.args)
    except pydantic.ValidationError as e:
        return Response(status=422, response=str(e))
    if d not in word_list_store:
        word_list_store[d] = None
        executor.submit(_generate_preview, d)
        time.sleep(0.1)  # trick to make cached requests short-circuit poll
    if word_list_store[d] is None:
        return Response(status=202, response="{}")
    wordlist = word_list_store[d]
    return render_template("preview.html", wordlist=wordlist, d=d)


@app.post("/api/generate/full")
def generate_full():
    try:
        d = schema.GenerateDeckSchema(**request.json)
    except pydantic.ValidationError as e:
        return Response(status=422, response=str(e))
    if d not in deck_store:
        deck_store[d] = {"status": "IN_PROGRESS", "message": "Processing..."}
        executor.submit(_generate_full, d)
        time.sleep(0.1)  # trick to make cached requests short-circuit poll
    if deck_store[d]["status"] == "IN_PROGRESS":
        return make_response({"message": deck_store[d]["message"]}, 202)
    elif deck_store[d]["status"] == "ERROR":
        return make_response({"message": deck_store[d]["message"]}, 500)
    elif deck_store[d]["status"] == "DONE":
        return Response(
            status=200,
            response="{}",
            headers={
                "Location": "/decks/" + basename(deck_store[d]["filename"])
            },
        )
    else:
        raise ValueError(f"Unknown status: {deck_store[d]['status']}")


def _generate_full(d: schema.GenerateDeckSchema):
    try:
        t_start = time.perf_counter()
        logging.info(
            f"Generating full deck for [{d.topic}, {d.native}, {d.target}, {d.extra}, {d.count}, {d.target_tts}, {d.native_tts}, {d.boost_extra}]"
        )
        wordlist = gen_wordlist(d.topic, d.native, d.target, d.extra, d.count)
        target_sounds = d.target_tts and get_sounds(
            d.target,
            [word.original for word in wordlist.words],
            [word.extra for word in wordlist.words],
            lambda msg: _update_progress(d, msg),
        )
        native_sounds = d.native_tts and get_sounds(
            d.native,
            [word.meaning for word in wordlist.words],
            feedback_cb=lambda msg: _update_progress(d, msg),
        )
        package = make_deck(
            wordlist, d.topic, target_sounds, native_sounds, d.boost_extra
        )
        basename_sanitized = re.sub(r"\W+", "_", d.topic)
        filename = save_deck(package, basename_sanitized, "/var/decks")
        t_end = time.perf_counter()
        logging.info(f"Deck generated in {t_end - t_start:.2f}s: {filename}")
        deck_store[d] = {
            "status": "DONE",
            "message": "Deck generated",
            "filename": filename,
        }
    except Exception as e:
        deck_store[d] = {"status": "ERROR", "message": str(e)}


def _update_progress(d: schema.GenerateDeckSchema, msg: str):
    deck_store[d]["message"] = msg


@app.route("/download")
def download():
    try:
        d = schema.GenerateDeckSchema(**request.args)
    except pydantic.ValidationError as e:
        return Response(status=422, response=str(e))
    return render_template("download.html", d=d)


@app.route("/decks/<path:path>")
def download_link(path):
    return send_from_directory("/var/decks", path)
