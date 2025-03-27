from openai import OpenAI

client = None

def openai_client():
    global client
    if client is None:
        client = OpenAI()
    return client
