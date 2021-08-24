from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# These args will get passed on to the python operator
default_args = {
    'owner': 'lakshay',
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
def my_function(x):
    return x + " is a must have tool for Data Engineers."


# define the DAG
dag = DAG(
    'python_operator_sample',
    default_args=default_args,
    description='How to use the Python Operator?',
    schedule_interval=timedelta(days=1),
)


# define the first task
t1 = PythonOperator(
    task_id='print',
    python_callable= my_function,
    op_kwargs = {"x" : "Apache Airflow"},
    dag=dag,
)

t1
