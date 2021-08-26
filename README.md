# Mazer - Airflow Mazes Scrapper

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

