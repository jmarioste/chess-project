
from os import listdir, path
# from PIL import Image
# from io import BytesIO
import re
import base64


def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [int(c) if c.isdigit() else c for c in re.split('([0-9]+)', s)]


def get_filenames_from_dir(mypath):
    return [f for f in listdir(mypath) if path.isfile(path.join(mypath, f))]


def get_lines_from_file(file_path):
    file1 = open(file_path, 'r')
    lines = file1.readlines()
    return lines


def img_to_base64(file_path):

    with open(file_path, "rb") as file:
        base64 = base64.b64encode(file.read()).decode('ascii')

    return str_msg
