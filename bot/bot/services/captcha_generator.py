from io import BytesIO
import random
import string

from aiogram.types import InputFile
from captcha.image import ImageCaptcha


def generate_captcha(captcha_size: int = 6) -> dict:
    captcha: str = ''.join(
        random.choices(string.ascii_letters + string.digits, k=captcha_size))

    image = ImageCaptcha(width=850, height=472, font_sizes=[150, 160, 170])
    return {
        'img': wrap_media(image.generate(captcha)),
        'key': captcha
    }


def get_captcha_image_with_buttons():
    captcha = generate_captcha()

    captcha_options = [''.join(
        random.choices(
            string.ascii_letters + string.digits, k=6)) for _ in range(3)]
    captcha_options.append(captcha['key'])
    random.shuffle(captcha_options)

    return captcha, captcha_options


def wrap_media(bytesio: BytesIO) -> InputFile:
    bytesio.seek(0)
    return InputFile(bytesio)
