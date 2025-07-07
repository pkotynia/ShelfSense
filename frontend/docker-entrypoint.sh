#!/bin/sh
# This script replaces the API URL in the frontend assets with the value from API_URL env variable
# then starts the Nginx server

# Replace API URL in all JavaScript files
find /usr/share/nginx/html -name "*.js" -exec sed -i "s|http://localhost:8000|${API_URL:-http://localhost:8000}|g" {} \;

# Start Nginx
exec nginx -g "daemon off;"
