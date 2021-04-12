FROM python:3.8-slim-buster
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . /app
ENTRYPOINT [ "python3" ]
CMD [ "string_gen.py" ]