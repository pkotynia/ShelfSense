# Use Node.js LTS as the base image
FROM node:20-alpine as build

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy the rest of the frontend code
COPY . .

# Build the application for production
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy the build output from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx config if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN apk add --no-cache dos2unix \
   && dos2unix /docker-entrypoint.sh \
   && chmod +x /docker-entrypoint.sh

# Expose port 80 (Nginx default)
EXPOSE 80

# Start Nginx with the custom entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]
