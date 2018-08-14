FROM alpy

RUN apk add git py3-pillow
RUN pip install -t $(pwd) git+https://github.com/timothycrosley/hug

COPY ./requirements.txt /
RUN pip install -r requirements.txt

COPY ./rsj /rsj
WORKDIR /rsj

EXPOSE 8000
#CMD python3 rsj.py

ENTRYPOINT ["hug", "-f", "rsj.py"]
