[![Maintainability](https://api.codeclimate.com/v1/badges/5c9be06a382901592e89/maintainability)](https://codeclimate.com/github/chidioguejiofor/airtech-api/maintainability) [![Maintainability](https://api.codeclimate.com/v1/badges/5c9be06a382901592e89/maintainability)](https://codeclimate.com/github/chidioguejiofor/airtech-api/maintainability)

# Airtech API
has had their challenges using spreadsheets to manage their flight booking system. They are ready to automate their processes with an application and have reached out to you to build a flight booking application for the company.

## Setup App
Run the following commands:

- Clone repo via git clone `https://github.com/chidioguejiofor/InitialisePythonProject.git`
- Start virtual environment via `pipenv shell`
- Install dependencies via `pipenv install`
- Make bash scripts executable via: ` chmod +x hooks/install_hooks.sh hooks/pre_commit.sh`
- Install hooks by running: `hooks/install_hooks.sh`

## Starting the app
In order to start the app locally, run `python manage.py runserver`. 
You can test the endpoints in the postman documentation  here [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/2ed3253e6a165822c4c6)

## Running Tests
You can run tests for the app via: `pytest --cov=airtech_api --cov-report=html`

