FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7-alpine3.8

COPY ./requirements.txt /requirements.txt
RUN pip install -U pip
# required for pillow installation
RUN apk add --no-cache zlib-dev jpeg-dev musl-dev gcc
RUN pip install -r /requirements.txt

# COPY ./rsj/ /app/

CMD /start-reload.sh
