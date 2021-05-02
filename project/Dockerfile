FROM python:3.8-slim-buster
WORKDIR /usr/src/app
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
