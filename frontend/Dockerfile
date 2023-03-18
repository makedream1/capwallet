FROM node:18-alpine as builder

WORKDIR /

COPY public /public/
COPY package.json package-lock.json tsconfig.json /

RUN npm install

COPY src /src/
RUN npm run build


FROM nginx:alpine

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY /etc/letsencrypt/live/volreviews.com/fullchain.pem /etc/nginx/certs/fullchain.pem
COPY /etc/letsencrypt/live/volreviews.com/privkey.pem /etc/nginx/certs/privkey.pem

COPY --from=builder /build /usr/share/nginx/html

EXPOSE 80 443