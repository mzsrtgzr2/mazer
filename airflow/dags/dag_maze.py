from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago

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


# define the python function
def fetch_maze():
    pass

def create_page_img():
    pass

def generate_pdf():
    pass


mazes_width = int(Variable.get('mazes_width', default_var=15))
pdf_pages = int(Variable.get('pdf_pages', default_var=10))

# define the DAG
with DAG(
    'mazes_pdf',
    default_args=default_args
) as dag:

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    generate_pdf = PythonOperator(
            task_id='generate_pdf',
            python_callable= generate_pdf
        )
    

    for page_num in range(pdf_pages):
        start >> PythonOperator(
            task_id=f'fetch_maze_{page_num}',
            python_callable= fetch_maze
        ) >> PythonOperator(
            task_id=f'create_page_img_{page_num}',
            python_callable= create_page_img
        ) >> generate_pdf
    
    generate_pdf >> end
