FROM node:14-alpine AS builder

RUN apk add --update python3 make g++ \
    && rm -rf /var/cache/apk/*


ENV JQ_VERSION=1.6
RUN wget --no-check-certificate https://github.com/stedolan/jq/releases/download/jq-${JQ_VERSION}/jq-linux64 -O /tmp/jq-linux64
RUN cp /tmp/jq-linux64 /usr/bin/jq
RUN chmod +x /usr/bin/jq

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json ./

RUN yarn install

COPY . .

RUN jq 'to_entries | map_values({ (.key) : ("$" + .key) }) | reduce .[] as $item ({}; . + $item)' ./src/config.json > ./src/config.tmp.json && mv ./src/config.tmp.json ./src/config.json


RUN yarn build

##############

FROM nginx:1.20.2-alpine
# Nginx config
RUN rm -rf /etc/nginx/conf.d
COPY conf /etc/nginx

COPY --from=builder /app/build /usr/share/nginx/html/

# Default port exposure
EXPOSE 3000

# Copy .env file and shell script to container
WORKDIR /usr/share/nginx/html
COPY ./env.sh .
COPY .env .

COPY ./start-nginx.sh .
RUN chmod +x start-nginx.sh


# Add bash
RUN apk add --no-cache bash

RUN chmod +x env.sh
ENV JSFOLDER=/usr/share/nginx/html/static/js/main*.js

CMD ["/bin/bash", "-c", "/usr/share/nginx/html/start-nginx.sh && /usr/share/nginx/html/env.sh && nginx -g \"daemon off;\""]