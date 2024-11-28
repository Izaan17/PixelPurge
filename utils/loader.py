import customtkinter
from PIL import Image


def load_image(path: str, size: tuple[int, int] = (20, 20)):
    return customtkinter.CTkImage(Image.open(path), size=size)