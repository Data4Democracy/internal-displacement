FROM node:latest

RUN mkdir /internal-displacement-web
WORKDIR /internal-displacement-web

COPY . /internal-displacement-web

RUN npm install
RUN cd /internal-displacement-web/client && npm install
RUN cd /internal-displacement-web/server && npm install

CMD npm run start
