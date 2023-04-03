# Base image
FROM node:14-alpine

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files

COPY . .

# Build the Vue.js application
RUN npm run build --verbose

# Expose the application port
EXPOSE 8080

# Start the application
CMD ["npm", "run", "start"]

