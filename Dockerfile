# Use the official Nginx image from the Docker Hub
FROM nginx:alpine

# Copy the content of the pages directory to the default nginx html location
COPY ./pages /usr/share/nginx/html

EXPOSE 80