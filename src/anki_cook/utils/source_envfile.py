import os


def source_envfile():
    try:
        with open(".env") as f:
            for line in f:
                key, value = line.strip().split("=")
                os.environ[key] = value
    except FileNotFoundError:
        pass
