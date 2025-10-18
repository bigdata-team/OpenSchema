FROM nginx:1.29.2-alpine 

COPY nginx.conf /etc/nginx/
COPY default.conf /etc/nginx/conf.d/
COPY api.conf /etc/nginx/conf.d/
COPY ui.conf /etc/nginx/conf.d/
COPY cert.pem /etc/ssl/certs/
COPY key.pem /etc/ssl/certs/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
