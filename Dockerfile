FROM python:3.9.1-slim-buster

RUN apt-get update -y

COPY ./buildfiles/get-docker.sh get-docker.sh
COPY ./buildfiles/get-nginx.sh get-nginx.sh

RUN sh get-docker.sh
RUN sh get-nginx.sh

RUN pip3 install \
    pipenv \
    certbot-nginx

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --system

COPY ./sharpnet /sharpnet/

ENTRYPOINT ["python3.9"]
CMD ["-um", "sharpnet"]