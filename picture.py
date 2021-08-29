# import external python modules
import random
import os
import pyheif
from PIL import Image

# impor internal python modules
from logger import logger as log

def random_image():
    # path = r"/home/slmansfield/my_twitterbot/images"
    path = r"images/"
    random_filename = random.choice(
        [x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))]
    )
    add_selected_image_to_log("image_log.txt", random_filename)
    log.info("Selected {} file".format(random_filename))
    return random_filename

def add_selected_image_to_log(log_file, image_filename):
    f = open(log_file, "a")
    f.write(image_filename + "\n")
    f.close()
    log.info("Updated the log file with the latest randomly selected image")
    return


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
