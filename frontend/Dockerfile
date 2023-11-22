## Build
FROM node:lts as builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . ./
RUN npm run generate

FROM nginx:mainline-alpine
COPY --from=builder /app/.output/public /usr/share/nginx/html
COPY default.conf /etc/nginx/conf.d/default.conf
