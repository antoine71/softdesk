# SOFTDESK

Openclassrooms - Parcours développement Python Projet 10

## Status

This project is under developement

## Description

SoftDesk est une API permettant de remonter et suivre des problèmes techniques (issue tracking system).

Softdesk is an API that allows user to create and track technical issues.

This API is designed to operate in the backend of iOS, Android or web applications. The applicaiton shall aloow users to create projects, add users, create issues and comments, assign priorities or tags etc.

The applications shall use termination points of the API to request and write data.

The documentation of the API is available at the following adress: [postman documentation](https://documenter.getpostman.com/view/14947762/TzCFgqFn)

## Installation

1. Clone this repository using `$ git clone https://github.com/antoine71/softdesk.git` (you can also download the code using [as a zip file](https://github.com/antoine71/softdesk/archive/main.zip))
2. Navigate to the root folder of the repository
3. Create a virtual environment with `python -m venv env`
4. Activate the virtual environment with `source env/bin/activate`
5. Install project dependencies with `pip install -r requirements.txt`
6. Run the server with `python manage.py runserver`

## Usage

1. The api can be queried from the following address : `http://localhost:8000/api/`
2. Refer to the API documentation for the list and description of all termination points: [postman documentation](https://documenter.getpostman.com/view/14947762/TzCFgqFn)
