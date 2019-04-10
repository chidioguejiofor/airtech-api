import dj_database_url
DATABASE_URI = 'postgres://postgres:password@db:5432/airtech_docker_db'
DATABASES = {'default': dj_database_url.parse(DATABASE_URI, conn_max_age=600)}
DEBUG = True
