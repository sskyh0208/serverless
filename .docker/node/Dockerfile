FROM node:20-alpine AS base

RUN apk add --no-cache bash curl gzip tar vim

COPY ./src/client /app
WORKDIR /app

# FROM base AS prod

# RUN npm install && npm run build

# CMD ["sh", "-c", "npm run start"]