# PDF Mazes generator

This code scraps mazes online, and create a simple PDF file to print.

- [PDF Mazes generator](#pdf-mazes-generator)
  - [Tech Stack](#tech-stack)
  - [Setup](#setup)
    - [Local run](#local-run)
    - [Run with Airflow](#run-with-airflow)

## Tech Stack
- Python 3.7
- Conda
- [Airflow](https://airflow.apache.org/) - schedule and monitor workflows
- Docker
- [Invoke](http://www.pyinvoke.org/)
- Beautifulsoup
- Pillow - image processing 


## Setup

Clone this GIT repo to your machine.

On the project root folder:

```
conda env create -f environment.yml
export AIRFLOW_HOME=$(PWD)/airflow

# create airflow.db
airflow db init

# create admin user for webserver access
airflow users create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin

```


### Local run

To generate mazes PDF locally run
```
inv run

Usage: inv[oke] [--core-opts] run [--options] [other tasks here ...]

Docstring:
  Create a pdf of mazes
  1. scrap mazes images from website
  2. create an image for every maze
  3. join all pages to a pdf

Options:
  -c INT, --count=INT
  -i STRING, --images-dir=STRING
  -o STRING, --out-pdf=STRING
  -w INT, --width=INT

```

### Run with Airflow

Airflow workflow consists the following tasks:
- Task 1 - scrap maze website for a new maze
- Task 2 - generate images as pages 
- Task 3 - create a PDF from images

Shell #1:
```
AIRFLOW_HOME=$(PWD)/airflow airflow scheduler
```


Shell #2:
```
AIRFLOW_HOME=$(PWD)/airflow airflow webserver
```

Go to http://localhost:8080
logon with admin:admin, find `mazes_pdf` DAG, enable it and run it. The `mazes.pdf` file should be generated in the folder. 





