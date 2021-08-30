from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
import os
import sys
import inspect
import time
from fpdf import FPDF
from os import listdir, remove
from os.path import isfile, join
import tempfile
import random


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 


from src.scrapper import generate_maze
from src.proc_maze import proc_maze
from src.cleanup import cleanup

DEFAULT_PRIZE_IMAGES_DIR = '../../images/ziv'
DEFAULT_PDF_OUTPUT = join(currentdir, '../..', 'mazes.pdf')


PRIZES_PATH = join(currentdir, DEFAULT_PRIZE_IMAGES_DIR)
PRIZE_IMAGES = tuple(
    join(PRIZES_PATH, f)
    for f in listdir(PRIZES_PATH)
    if isfile(join(PRIZES_PATH,f))
)

ts = int(time.time())

# These args will get passed on to the python operator
default_args = {
    'owner': 'moshe',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

def _get_ret_val_from_task(kwargs, task_id):
    return kwargs['ti'].xcom_pull(key=None, task_ids=[task_id])[0]


# define the python function
def fetch_maze(num, width):
    return next(generate_maze(f'mazeid_{num}', width))

def create_page_img(num, **kwargs):
    maze_url = _get_ret_val_from_task(
        kwargs,
        f'{fetch_maze.__name__}_{num}')
    
    print('processing', maze_url)
    
    dest = join(
            tempfile.gettempdir(),
            f'maze_{ts}_{num}.png')
    
    proc_maze(maze_url, random.choice(PRIZE_IMAGES), dest)
    
    return dest


def generate_pdf(pdf_pages, **kwargs):
    # pulled_value_2 = ti.xcom_pull(task_ids='push_by_returning')
    pdf = FPDF()

    finals = []
    for page in range(pdf_pages):
        image = _get_ret_val_from_task(
            kwargs,
            f'{create_page_img.__name__}_{page}')
        print('adding page', image)
        pdf.add_page()
        pdf.image(image,0, 0,210,280)

        finals.append(image)

    pdf.output(DEFAULT_PDF_OUTPUT, 'F')
    cleanup(finals)


mazes_width = int(Variable.get('mazes_width', default_var=15))
pdf_pages = int(Variable.get('pdf_pages', default_var=50))

# define the DAG
with DAG(
    'mazes_pdf',
    default_args=default_args
) as dag:

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    generate_pdf = PythonOperator(
            task_id='generate_pdf',
            python_callable= generate_pdf,
            op_kwargs={'pdf_pages': pdf_pages},
            provide_context=True,
        )
    

    for page_num in range(pdf_pages):
        start >> PythonOperator(
            task_id=f'fetch_maze_{page_num}',
            python_callable= fetch_maze,
            provide_context=True,
            op_kwargs={'num': page_num, 'width': mazes_width},
        ) >> PythonOperator(
            task_id=f'create_page_img_{page_num}',
            python_callable   = create_page_img,
            op_kwargs={'num': page_num},
            provide_context=True,
        ) >> generate_pdf
    
    generate_pdf >> end
