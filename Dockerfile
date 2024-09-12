# Use the official Nginx image from the Docker Hub
FROM nginx:alpine

# Remove the default Nginx config file
RUN rm /etc/nginx/conf.d/default.conf

# Copy your custom Nginx config file
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Copy the content of the pages directory to the Nginx html directory
COPY ./pages /usr/share/nginx/html

EXPOSE 80