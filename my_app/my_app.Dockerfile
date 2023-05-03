# Step 1 - Build vue project
FROM node:12.18.1-alpine AS build
WORKDIR /usr/src/app/my_app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "run", "serve"]