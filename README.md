# PDF Mazes generator

This code scraps mazes online, and create a simple PDF file to print.

## Tech Stack
- Python 3.7
- Conda
- [Airflow](https://airflow.apache.org/) - schedule and monitor workflows
- Docker
- [Invoke](http://www.pyinvoke.org/)
- Beautifulsoup
- Pillow - image processing 


## Setup

Setup python environment with conda
```
conda env create -f environment.yml
export AIRFLOW_HOME=$(PWD)/airflow

# create airflow.db
airflow db init

# create admin user for webserver access
airflow users create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin

```

### Run

Shell #1:
```
AIRFLOW_HOME=$(PWD)/airflow airflow scheduler
```


Shell #2:
```
AIRFLOW_HOME=$(PWD)/airflow airflow webserver
```


### Airflow DAG
Task 1 - scrap maze website for a new maze
Task 2 - generate images as pages 
Task 3 - create a PDF from images


# Local run

To generate maze locally run
```
inv local-run
```


