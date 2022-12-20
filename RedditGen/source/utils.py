import string
import random
import requests

def random_char(yrange):
    return ''.join(random.choice(string.ascii_letters) for y in range(yrange))

def namorator():
    r = requests.get("https://apis.kahoot.it/namerator")
    name = r.json()["name"]
    username = name + random_char(5)
    return username
