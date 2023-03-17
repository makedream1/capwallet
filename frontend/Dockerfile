FROM node:18-alpine as build

WORKDIR /

COPY public /public/
COPY package.json package-lock.json tsconfig.json /

RUN npm install

COPY src /src/
RUN npm run build
