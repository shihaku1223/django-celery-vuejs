FROM nginx

COPY ./dist /usr/share/web
COPY ./web.conf /etc/nginx/conf.d/web.conf

EXPOSE 8080
