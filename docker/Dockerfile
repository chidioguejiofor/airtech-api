
FROM python:3.7.2
RUN pip install pipenv

WORKDIR /airtech-api
COPY ./Pipfile /airtech-api
COPY ./Pipfile.lock /airtech-api

RUN pipenv install --system  --deploy --ignore-pipfile

ADD scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

COPY . /airtech-api

EXPOSE 7000

ENTRYPOINT ["entrypoint.sh"]
