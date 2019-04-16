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
ADD  ./docker-heroku/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copy all the other files/folders to airtech-api
COPY . /airtech-api

USER root

# Start app by running entrypoint.sh bash script
CMD bash docker-heroku/entrypoint.sh
