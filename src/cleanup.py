from os import remove

def cleanup(files: Sequence[str]):
    for file in finals:
        remove(file)