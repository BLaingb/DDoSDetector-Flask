FROM ubuntu:16.04

RUN apt-get update -y && \
	apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN python3 --version

RUN pip3 install -r requirements.txt

COPY . / 

ENTRYPOINT [ "python3" ]

CMD ["main.py"]
