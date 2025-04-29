# ビルド用ステージ
FROM node:16-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# 実行用ステージ
FROM nginx:stable-alpine
# 先ほど作った設定をデフォルトに上書き
COPY nginx.conf /etc/nginx/conf.d/default.conf
# 静的ファイルを配置
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
