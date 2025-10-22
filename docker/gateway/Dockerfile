FROM nginx:1.29.2-alpine 

COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/
COPY certs/ /etc/nginx/certs/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
