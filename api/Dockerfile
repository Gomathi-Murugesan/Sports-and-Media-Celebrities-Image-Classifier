FROM python:3.7

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY ./requirements.txt /tmp/requirements.txt
WORKDIR /tmp
RUN pip install -r requirements.txt

COPY . /api
WORKDIR /

CMD ["gunicorn", "-w", "3", "-b", ":5001", "-t", "360", "--reload", "api.wsgi:app"]

#CMD ["gunicorn", "-w", "3", "-b", --port $PORT, "-t", "360", "--reload", "api.wsgi:app"]
#CMD gunicorn --workers=4 --bind 0.0.0.0:5001 api1.wsgi:app -t 360 --reload