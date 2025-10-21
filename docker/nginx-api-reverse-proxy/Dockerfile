FROM nginx:alpine

COPY docker/nginx-api-reverse-proxy/nginx/nginx.conf /etc/nginx/nginx.conf
COPY docker/nginx-api-reverse-proxy/nginx/conf.d/ /etc/nginx/conf.d/
COPY docker/nginx-api-reverse-proxy/nginx/certs/ /etc/nginx/certs/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
