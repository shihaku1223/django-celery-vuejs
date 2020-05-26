FROM python:3.7.7

ENV http_proxy http://proxy.olympus.co.jp:8080
ENV https_proxy http://proxy.olympus.co.jp:8080

ADD app.py /
ADD requirements.txt /

RUN pip install \
  --index-url  http://10.156.2.65/ipf3-offshore/pypi/ \
  --trusted-host 10.156.2.65 -r requirements.txt

VOLUME ["/tmp/tfhub_modules"]

WORKDIR /
ENTRYPOINT ["python", "app.py"]
CMD ["--help"]
