FROM nginx:1.19

RUN apt-get update -y && \
    apt-get install -y moreutils gettext-base

RUN apt-get install -y \
    python3.7 \
    python3-pip \
    python3-certbot-nginx &&\
    pip3 install flask

COPY ./buildfiles/manager.py manager.py

CMD [ "python3", "-u", "./manager.py" ]