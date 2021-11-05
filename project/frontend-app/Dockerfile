FROM node:14-alpine
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
RUN apk add --update python3 make g++\
   && rm -rf /var/cache/apk/*
COPY package.json ./
COPY package-lock.json ./
RUN npm install
COPY . ./
CMD ["npm", "start"]