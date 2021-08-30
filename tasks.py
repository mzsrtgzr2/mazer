from invoke import task
from typing import Sequence, Optional
import inspect
import os
from os.path import join
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

DEFAULT_PRIZE_IMAGES_DIR = join(currentdir, 'images/ziv')
DEFAULT_PDF_OUTPUT = join(currentdir, 'mazes.pdf')

@task
def run(ctx,
        width = 20,
        count = 5,
        images_dir = None,
        out_pdf = None
        ):
    
    """
    Create a pdf of mazes
    1. scrap mazes images from website
    2. create an image for every maze 
    3. join all pages to a pdf

    """

    from fpdf import FPDF
    from os import listdir, remove
    from os.path import isfile, join
    import tempfile
    import time
    from airflow.src.scrapper import generate_maze
    from airflow.src.proc_maze import proc_maze
    from airflow.src.cleanup import cleanup

    mazes_urls = tuple(generate_maze('maze', width, count))

    finals = []
    images_dir = images_dir or DEFAULT_PRIZE_IMAGES_DIR

    onlyfiles = [join(images_dir, f) 
        for f in listdir(images_dir) if isfile(join(images_dir, f))]

    ts = int(time.time())
    for i, (maze_url, prize_image) in enumerate(zip(mazes_urls, onlyfiles)):
        if not prize_image or not maze_url:
            break
        dest = join(
            tempfile.gettempdir(),
            f'maze_{ts}_{i}.png')
    
        proc_maze(maze_url, prize_image, dest)
        finals.append(dest)

    
    pdf = FPDF()
    # imagelist is the list with all image filenames
    for i, image in enumerate(finals):
        pdf.add_page()
        pdf.image(image,0, 0,210,280)

    file = out_pdf or DEFAULT_PDF_OUTPUT
    pdf.output(file, "F")
    print('created pdf file', file)

    cleanup(finals)



