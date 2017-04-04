FROM node:latest

RUN mkdir /internal-displacement-web
WORKDIR /internal-displacement-web

COPY . /internal-displacement-web

RUN yarn install
RUN cd /internal-displacement-web/client && yarn install
RUN cd /internal-displacement-web/server && yarn install

CMD npm run start
