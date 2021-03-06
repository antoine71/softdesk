# SOFTDESK

Openclassrooms - Parcours développement Python Projet 10

## Status

This project is ready for evaluation.

## Description

Softdesk is an API that allows users to create and track technical issues.

This API is designed to operate in the backend of an iOS, Android or web application. The application shall allow users to create projects, add collaborators, create issues and comments, assign priorities or tags etc.

The application shall use the termination points of the API to request and write data.

The documentation of the API is available at the following location: [postman documentation](https://documenter.getpostman.com/view/14947762/TzCFgqFn)

The API is developped in python using Django Rest Framework.

## Installation

Python 3 is required to run the API.

1. Clone this repository using `$ git clone https://github.com/antoine71/softdesk.git` (you can also download the code using [as a zip file](https://github.com/antoine71/softdesk/archive/main.zip))
2. Navigate to the root folder of the repository
3. Create a virtual environment with `python -m venv env`
4. Activate the virtual environment with `source env/bin/activate`
5. Install project dependencies with `pip install -r requirements.txt`
6. Run the server with `python manage.py runserver`

## Usage

1. The api can be queried from the following address : `http://localhost:8000/api/`
2. Refer to the API documentation for the list and description of all termination points: [postman documentation](https://documenter.getpostman.com/view/14947762/TzCFgqFn)
