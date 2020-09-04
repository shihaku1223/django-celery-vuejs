FROM python:3.7.7

ENV http_proxy http://proxy.olympus.co.jp:8080
ENV https_proxy http://proxy.olympus.co.jp:8080
ENV DIR /var/lib/similarityapp

WORKDIR ${DIR}
ADD requirements.txt ${DIR}

RUN pip install \
    --index-url  http://10.155.47.34/ipf3-offshore/pypi/ \
    --trusted-host 10.155.47.34 -r requirements.txt

ADD uwsgi.ini ${DIR}
ADD similarityapp ${DIR}

RUN python manage.py collectstatic --noinput

ENTRYPOINT []
CMD python manage.py makemigrations \
  && python manage.py migrate \
  && python manage.py runserver 0:8000
