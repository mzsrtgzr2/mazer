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
    end_img = Image.open(prize_image, 'r')
    orig_size = end_img.size
    end_img.thumbnail((prize_size, int(prize_size*orig_size[1]/orig_size[0])), Image.ANTIALIAS)
    w, h = end_img.size
    background.paste(end_img, (bg_w//2 - w//2, arrow_size + maze.size[1] + 30))

    background.save(dest)