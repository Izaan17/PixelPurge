import os

HOME_PATH = os.path.expanduser('~')
PIXEL_PURGE_FOLDER = os.path.join(HOME_PATH, 'PixelPurge')
PIXEL_PURGE_DIRECTORIES_FILE = os.path.join(PIXEL_PURGE_FOLDER, 'directories.json')
DEFAULT_DIRECTORIES = [os.path.join(HOME_PATH, 'AppData')]
IS_MAC = os.uname().sysname == 'Darwin'