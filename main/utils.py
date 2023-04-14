import string
import random
import qrcode


def code_generator(length: int):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(length))


def qrcode_generate(link, img_path):
    img = qrcode.make(link)
    file = open("..\media\codes\\"+img_path, "wb")
    file.close()
    img.save("..\media\codes\\"+img_path)


#qrcode_generate("http://127.0.0.1:8000/get_code/"+"XFS5DSH", "XFS5DSH"+".png")
