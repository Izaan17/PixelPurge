import os.path

import customtkinter
from PIL import Image

from utils.directory import get_icon_dir


def load_image(path: str, size: tuple[int, int] = (20, 20)):
    return customtkinter.CTkImage(Image.open(path), size=size)

def load_icon(path: str, size: tuple[int, int] = (20, 20)):
    return load_image(os.path.join(get_icon_dir(), path), size=size)