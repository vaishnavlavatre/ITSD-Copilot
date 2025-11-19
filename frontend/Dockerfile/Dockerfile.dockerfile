FROM nginx:alpine

# Copy static files
COPY static /usr/share/nginx/html/static
COPY templates /usr/share/nginx/html/templates

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]