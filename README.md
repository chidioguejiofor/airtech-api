[![Maintainability](https://api.codeclimate.com/v1/badges/5c9be06a382901592e89/maintainability)](https://codeclimate.com/github/chidioguejiofor/airtech-api/maintainability) [![Maintainability](https://api.codeclimate.com/v1/badges/5c9be06a382901592e89/maintainability)](https://codeclimate.com/github/chidioguejiofor/airtech-api/maintainability)

# Airtech API
has had their challenges using spreadsheets to manage their flight booking system. They are ready to automate their processes with an application and have reached out to you to build a flight booking application for the company.

## Setup App
Run the following commands:

- Clone repo via git clone `https://github.com/chidioguejiofor/airtech-api.git`
- Start virtual environment via `pipenv shell`
- Install dependencies via `pipenv install`
- Make bash scripts executable via: ` chmod +x hooks/install_hooks.sh hooks/pre_commit.sh`
- Install hooks by running: `hooks/install_hooks.sh`
- Use the `.env-sample` file to create a `.env` file with required environmental variables

## Linting Automation
The app is configured to automatically lint your files once you do a `git commit`. However you can decide to lint all 
python files by running `yapf -ir $(find . -name '*.py')`. 
Linting follows the [PE8 Style Guide](https://www.python.org/dev/peps/pep-0008/)


## Starting the app
In order to start the app locally, run `python manage.py runserver`. 

## Documentation
You can all the endpoints in the postman documentation  here [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/2ed3253e6a165822c4c6)

## Starting Redis and Celery
Celery is used as the message broker for the API. We use it to run heavy task(via celery-workers) and run cronjobs(via celery-beat).

#### Starting Redis
In order to run celery, you would need to ensure that a `redis` is running. 
Using docker, you can achieve this by running `docker run -p 6379:6379 redis`. This would spin up a redis server in  port `6379` in your machine.

If your `redis server` is running on a different port/host, you must specify the URL in the `.env` file via key `REDIS_SERVER_URL`

#### Starting Redis
Once Redis is up and running, you can now spin up celery in these steps:

- Start celery worker by executing  `celery -A celery_config.celery_app worker --loglevel=info`
- In a separate terminal, spin up the celery beat via `celery -A celery_config.celery_schedules beat --loglevel=info`

## Docker Setup
You could also easily start the API, Celery and Redis by using docker in the following steps:

1. Download and Install Docker from [Docker Getting Started Page](https://www.docker.com/get-started)
2. Ensure that Docker is installed by running `docker --version`. This should display the version of docker on your machine
3. In Project directory, use _docker-compose_ to build the app  by running  `docker-compose build`.
4. Start the app via `docker-compose up`. You could add the `-d`(`docker-compose -d`) if you don't want to see the logs of the app.
5. Run` docker ps` to see that the airtech app is running
6. You should be able to connect to the app via the `localhost`

When you are done running your app with docker, it is best to free up resources that is used. To do this follow these steps:

1. Make the *free_up_memory.sh* bash script executable by running `chmod +x scripts/free_up_memory.sh`
2. Execute the script via: `scripts/free_up_memory.sh`

The above would free up memory that is used in your docker instance

## Running Tests
You can run tests for the app via: `pytest --cov=airtech_api --cov-report=html`

