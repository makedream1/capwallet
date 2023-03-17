FROM nginx:latest

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./fullchain.pem /etc/ssl/certs/fullchain.pem
COPY ./privkey.pem /etc/ssl/certs/privkey.pem
COPY ./options-ssl-nginx.conf /etc/letsencrypt/options-ssl-nginx.conf
COPY ./ssl-dhparams.pem /etc/letsencrypt/ssl-dhparams.pem

EXPOSE 80 443