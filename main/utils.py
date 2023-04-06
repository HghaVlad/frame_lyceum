import string
import random


def code_generator(length: int):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))
