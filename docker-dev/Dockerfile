# Get Base image
FROM python:3.7.2

MAINTAINER Prof<chidioguejiofor@gmail.com>

# Install pipenv using pip
RUN pip install pipenv

# Make /airtech-api the working directory
WORKDIR /airtech-api

# Copy ./Pipfile and ./Pipfile.lock to the working directory
COPY ./Pipfile /airtech-api
COPY ./Pipfile.lock /airtech-api

# Install dependencies in the Pipfile
RUN  pipenv install --system  --deploy --ignore-pipfile

# Copy all the other files/folders to airtech-api
COPY . /airtech-api

# Make the scripts/entrypoint.sh bash script
ADD  docker-dev/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Create non-super user. This user would be used to run celery_config later on
RUN groupadd -g 999 appuser && \
    useradd -r -u 999 -g appuser celery_user

USER root

# Expose port 7000 to the world
EXPOSE 7000

# Start app by running entrypoint.sh bash script
ENTRYPOINT ["entrypoint.sh"]
