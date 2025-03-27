import os


def load_template(key):
    with open(
        os.path.join(os.path.dirname(__file__), "../templates", key + ".html")
    ) as f:
        return f.read()


def load_style():
    with open(
        os.path.join(os.path.dirname(__file__), "../templates", "style.css")
    ) as f:
        return f.read()
