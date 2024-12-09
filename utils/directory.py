from pathlib import Path


def get_project_root():
    """Get the path of the project master directory."""
    return Path(__file__).parent.parent\

def get_app_dir():
    app_dir = Path.home() / 'PixelPurge'
    return app_dir

def get_icon_dir():
    return get_project_root() / 'icons'
