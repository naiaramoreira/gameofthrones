FROM python:3.8

WORKDIR /code
COPY . /code

RUN apt-get update

RUN apt-get install -y build-essential && \
    apt-get install -y python-dev && \
    apt-get install -y libpq-dev && \
    apt-get install -y iputils-ping

RUN mkdir /var/code/flask_venv -p

RUN python3 -m venv /var/code/flask_venv

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN source /var/code/flask_venv/bin/activate

RUN pip install -r /code/requirements.txt

EXPOSE 5000
CMD python3 app.py