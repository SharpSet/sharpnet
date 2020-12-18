FROM nginx:1.19

RUN apt-get update -y

COPY get-docker.sh get-docker.sh
RUN sh get-docker.sh

RUN apt-get install -y \
    moreutils \
    gettext-base \
    python3.7 \
    python3-pip \
    python3-certbot-nginx

COPY ./source /source

CMD [ "python3", "-u", "/source/app.py" ]