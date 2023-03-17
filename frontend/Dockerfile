FROM node:18-alpine as builder

WORKDIR /

COPY public /public/
COPY package.json package-lock.json tsconfig.json /

RUN npm install

COPY src /src/
RUN npm run build


FROM nginx:alpine

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
# COPY ./fullchain.pem /etc/ssl/certs/fullchain.pem
# COPY ./privkey.pem /etc/ssl/certs/privkey.pem
# COPY ./options-ssl-nginx.conf /etc/letsencrypt/options-ssl-nginx.conf
# COPY ./ssl-dhparams.pem /etc/letsencrypt/ssl-dhparams.pem

COPY --from=builder /build /usr/share/nginx/html

EXPOSE 80 443