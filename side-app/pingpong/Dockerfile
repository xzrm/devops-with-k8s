FROM python:3.9
WORKDIR /usr/src/app
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
ENTRYPOINT [ "python3" ]
CMD [ "pingpong.py" ]