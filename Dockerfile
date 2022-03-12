FROM python:3.8
ENV PYTHONUNBUFFERED 1

WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD gunicorn core.wsgi:application — bind 0.0.0.0:$PORT

