FROM nginx:alpine

COPY docker/nginx-ui-reverse-proxy/nginx/nginx.conf /etc/nginx/nginx.conf
COPY docker/nginx-ui-reverse-proxy/nginx/conf.d/ /etc/nginx/conf.d/
COPY docker/nginx-ui-reverse-proxy/nginx/certs/ /etc/nginx/certs/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
