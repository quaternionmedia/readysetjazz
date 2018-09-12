FROM harpo1224/alpy

RUN apk add git py3-pillow nginx openrc uwsgi g++ linux-headers
RUN pip install -t $(pwd) git+https://github.com/timothycrosley/hug

COPY ./requirements.txt /
RUN pip install -r requirements.txt

<<<<<<< HEAD
COPY ./rsj /rsj/
# WORKDIR /rsj
=======
#COPY ./rsj /rsj

WORKDIR /rsj
>>>>>>> 7e52452d5a1d63e34ec613443db43159443aa8e7

EXPOSE 8000
#CMD python3 rsj.py

# ENTRYPOINT ["hug", "-f", "rsj.py"]

#RUN pip install uwsgi
RUN mkdir -p /run/nginx
RUN mkdir -p /run/openrc && touch /run/openrc/softlevel
COPY ./nginx.conf /etc/nginx/nginx.conf
RUN mkdir /socks
RUN adduser -D -g 'www' www
RUN mkdir /www && chown -R www:www /var/lib/nginx && chown -R www:www /www && chown -R www:www /rsj && chown -R www:www /socks
#RUN rc-service nginx start
# RUN nginx
RUN apk add libc-dev uwsgi-python3
# RUN uwsgi /rsj/rsj.ini
# ENTRYPOINT ["sh"]
# USER www
# RUN "uwsgi \
# 	--http-socket /socks/rsj.sock \
# 	--plugin python3 \
# 	--wsgi-file /rsj/rsj.py \
# 	--master \
# 	--processes 4 \
# 	--threads 2"
# 	#--stats /socks/stats.sock

#ENTRYPOINT ["uwsgitop /socks/stats.sock"]
