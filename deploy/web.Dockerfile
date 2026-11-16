# 1단계: React 화면 빌드
FROM node:20-alpine AS build
WORKDIR /web
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# 2단계: nginx가 빌드 결과를 서비스하고 /api 요청은 FastAPI로 넘김
FROM nginx:1.27-alpine
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /web/dist /usr/share/nginx/html
EXPOSE 80
