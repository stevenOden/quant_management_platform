FROM node:20-alpine AS build

WORKDIR /app

ARG DASHBOARD_GATEWAY_SERVICE_URL
ENV VITE_DASHBOARD_GATEWAY_SERVICE_URL=$DASHBOARD_GATEWAY_SERVICE_URL

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build


FROM node:20-alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=build /app/dist ./dist

EXPOSE 3000

CMD ["serve", "-s", "dist", "-l", "3000"]