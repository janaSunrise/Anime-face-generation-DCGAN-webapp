import os

from . import SAVE_DIR

if __name__ == '__main__':
    os.makedirs(SAVE_DIR, exist_ok=True)
