# FROM python:3.9
# WORKDIR /usr/src/app

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# RUN apt-get update && apt-get install -y netcat

# RUN pip install --upgrade pip
# COPY ./requirements.txt ./requirements.txt
# RUN pip3 install -r requirements.txt
# EXPOSE 4222
# COPY . .

FROM node:alpine
WORKDIR /usr/src/app
COPY package* ./

RUN npm install

COPY . .

CMD ["npm", "start"]
