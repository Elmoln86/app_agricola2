# Stage 1: build
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci || npm install
COPY . .
# Se você usa Vite e precisa de variável:
# VITE_API_BASE será injetada na build a partir do ambiente do compose (Caddy usa domínio)
RUN npm run build

# Stage 2: serve estático
FROM nginx:alpine
# remove default site
RUN rm -f /etc/nginx/conf.d/default.conf
# copia dist e conf
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/site.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]


