import csv
import json
import csv
from argparse import ArgumentParser
import pandas as pd
import numpy as np
import re
import os
import time
from collections import defaultdict
import logging
import requests
import time
from PIL import Image
logger = logging.getLogger()

from bs4 import BeautifulSoup

from fetch_mazes import generate_maze

import os

local_dir = os.path.dirname(os.path.abspath(__file__))

def proc_maze(maze_image, prize_image, dest):
    print('create mze', maze_image, prize_image)
    maze = Image.open(maze_image, 'r')

    pdf_w = 210
    pdf_h = 300

    background = Image.new('RGBA', (pdf_w*4, pdf_h*4), (255, 255, 255, 255))
    bg_w, bg_h = background.size

    margin = int(bg_w*0.25)

    maze_y = margin
    area = (maze_y, maze_y, bg_w-maze_y, bg_w-maze_y)
    
    maze = maze.resize((bg_w-2*maze_y, bg_w-2*maze_y))
    
    background.paste(maze, area)

    
    arrow = Image.open('/Users/mosherot/workspace/maze/images/diagonal-arrow.png', 'r')
    arrow_size = margin
    area = (bg_w//2 - arrow_size//2, 0, bg_w//2 + arrow_size//2, margin)
    background.paste(arrow.resize((arrow_size, arrow_size)), area)

    prize_size = bg_w // 2
    end_img = Image.open('/Users/mosherot/workspace/maze/{}'.format(prize_image), 'r')
    orig_size = end_img.size
    end_img.thumbnail((prize_size, int(prize_size*orig_size[1]/orig_size[0])), Image.ANTIALIAS)
    w, h = end_img.size
    background.paste(end_img, (bg_w//2 - w//2, arrow_size + maze.size[1] + 30))

    background.save(dest)
    

if __name__ == '__main__':
    parser = ArgumentParser()
    # parser.add_argument("-i", "--in", dest="text_input", help="text input file", metavar="FILE")
    # parser.add_argument("-e", "--env", dest="env", help="env")
    # parser.add_argument("-a", "--app_id", dest="app_id", help="app id")
    # parser.add_argument("-t", "--topic_id", dest="topic_id", help="topic id")
    # parser.add_argument("-p", "--push", dest="force_push",  action='store_true', help="force push")
    # parser.add_argument("-g", "--instagram", dest="instagram",  action='store_true', help="create instagram posts")
    

    args = parser.parse_args()
    
    mazes_urls = []
    mazes_urls.extend(list(generate_maze('level1', 5,3)))
    mazes_urls.extend(list(generate_maze('level2', 7,3)))
    mazes_urls.extend(list(generate_maze('level2', 9,3)))
    # mazes_urls.extend(list(generate_maze('level2', 8,5)))
    # mazes_urls.extend(list(generate_maze('level3', 9,5)))
    # mazes_urls.extend(list(generate_maze('level4', 10,5)))
    # mazes_urls.extend(list(generate_maze('level5', 11, 10)))
    # mazes_urls.extend(list(generate_maze('level6', 12, 20)))
    mazes_urls.extend(list(generate_maze('level15', 14, 3)))
    mazes_urls.extend(list(generate_maze('level15', 15, 3)))
    mazes_urls.extend(list(generate_maze('level15', 16, 3)))
    
    # mazes_urls = ['/Users/mosherot/workspace/maze/fetch_mazes/downloads/maze_renamed_medium_0.png']

    # print(mazes_urls)
    finals = []
    from os import listdir
    from os.path import isfile, join

    prize_images_dir = 'images/ziv'
    onlyfiles = [join(prize_images_dir, f) 
        for f in listdir(prize_images_dir) if isfile(join(prize_images_dir, f))]

    for i, (maze_url, prize_image) in enumerate(zip(mazes_urls, onlyfiles)):
        if prize_image is None or maze_url is None:
            break
        dest = '/tmp/maze_page_{}.png'.format(i)
        proc_maze(maze_url, prize_image, dest)
        print(dest)
        finals.append(dest)

    from fpdf import FPDF
    pdf = FPDF()
    # imagelist is the list with all image filenames
    for i, image in enumerate(finals):
        pdf.add_page()
        pdf.image(image,0, 0,210,280)

    pdf.output("mazes.pdf", "F")





