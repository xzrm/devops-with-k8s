FROM node:14-alpine AS builder

RUN apk add --update python3 make g++ \
    && rm -rf /var/cache/apk/*


# ENV JQ_VERSION=1.6
# RUN wget --no-check-certificate https://github.com/stedolan/jq/releases/download/jq-${JQ_VERSION}/jq-linux64 -O /tmp/jq-linux64
# RUN cp /tmp/jq-linux64 /usr/bin/jq
# RUN chmod +x /usr/bin/jq

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json ./

RUN yarn install

COPY . .

# RUN jq 'to_entries | map_values({ (.key) : ("$" + .key) }) | reduce .[] as $item ({}; . + $item)' ./src/config.json > ./src/config.tmp.json && mv ./src/config.tmp.json ./src/config.json


RUN yarn build

##############

FROM nginx:1.20.2-alpine

RUN apk add --no-cache bash

RUN rm -rf /etc/nginx/conf.d
COPY conf /etc/nginx

COPY --from=builder /app/build /usr/share/nginx/html/

EXPOSE 3000

WORKDIR /usr/share/nginx/html

#this is relevanet for when there is .env file used
COPY ./env.sh .
COPY .env .

#replaces env vars in minified js file
COPY ./env_sub.sh .


RUN chmod +x env_sub.sh 
RUN chmod +x env.sh

ENV JSFOLDER=/usr/share/nginx/html/static/js/main*.js

CMD ["/bin/bash", "-c", "/usr/share/nginx/html/env_sub.sh && /usr/share/nginx/html/env.sh && nginx -g \"daemon off;\""]