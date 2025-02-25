# Use an official Nginx runtime as a parent image
FROM nginx:latest

# Copy the static files to the correct location
COPY index.html /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]