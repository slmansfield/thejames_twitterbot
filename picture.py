# import external python modules
import random
import os
import pyheif
from PIL import Image


def random_image():
    # path = r"/home/slmansfield/my_twitterbot/images"
    path = r"images/"
    random_filename = random.choice(
        [x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))]
    )
    return random_filename


def convert_heif_to_jpg(image_filename):
    heif_file = pyheif.read(image_filename)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    image.save("images/temp.jpg", "JPEG")


def getPicture():
    picture = random_image()
    convert_heif_to_jpg("images/" + picture)
    return
