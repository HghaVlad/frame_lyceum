import string
import random
import qrcode
from django.conf import settings


def code_generator(length: int):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(length))


def qrcode_generate(link, img_path):
    img = qrcode.make(link)
    file = open(settings.MEDIA_ROOT / "codes" / img_path, "wb")
    file.close()
    img.save(str(settings.MEDIA_ROOT / "codes" / img_path))

