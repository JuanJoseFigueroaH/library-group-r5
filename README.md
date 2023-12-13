# Library Group R5

## Description
API Books is an evaluation project proposed by Grupo R5 that covers specialized capabilities and services in the treatment and access to books through both internal and external repositories, such as Google Books and OpenLibra.

## Getting Started Installation
1. pre requirements
  OS: Linux - Ubuntu <optional>
3.	Installation process
```bash
pip3 install virtualenv
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements/development.txt

# to deactivate venv
deactivate
```
### Run
```bash
python main.py
```
## Build and Test
### Install Requirements Test
```bash
pip install -r requirements.txt
```
### Run Test
```bash
pytest -vs test
```
### Run Test and Coverage
```bash
pytest -v --cov src --cov-report html test
```
### Run Test and Coverage include file .coveragerc
```bash
pytest -v --cov src --cov-report html --cov-config=.coveragerc test
```
  
## Usage Example
- [`GRAPHQL`]()
-- Nota: Filtros validos para GET Book (id, title, subtitle, author, category, datetime_publication, editor, description)