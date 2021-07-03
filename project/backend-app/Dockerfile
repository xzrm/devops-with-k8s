FROM python:3.9
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

RUN pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

