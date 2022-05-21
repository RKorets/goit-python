FROM python:3.9.7

MAINTAINER Korets Roman "vip.korets@ukr.net"

COPY . /helper

WORKDIR /helper

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["main.py"]
