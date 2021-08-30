from os import remove
from typing import Sequence

def cleanup(files: Sequence[str]):
    for file in files:
        remove(file)