install certbor:
    sudo snap install --classic certbot
    sudo ln -s /snap/bin/certbot /usr/bin/certbot

create ssl certs:
    certbot certonly --standalone --preferred-challenges http -d volreviews.com

update ssl certs:
    sudo certbot renew --dry-run

copy ssl certs:
    cd /etc/letsencrypt/live/volreviews.com/
    cp privkey.pem fullchain.pem ~/CapWallet/frontend/nginx/

for build project:
    docker compose up -d --build

for shut down and delete project containers and volumes:
    docker-compose down --rmi all -v --remove-orphans