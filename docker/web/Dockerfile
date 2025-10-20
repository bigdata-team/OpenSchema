FROM node:22-alpine AS build

ARG BUILD_CONTEXT_PATH=src/web
ARG SERVICE_DIR

RUN corepack enable

WORKDIR /app
COPY ${BUILD_CONTEXT_PATH}/pnpm-workspace.yaml ${BUILD_CONTEXT_PATH}/package.json ${BUILD_CONTEXT_PATH}/pnpm-lock.yaml ./
COPY ${BUILD_CONTEXT_PATH}/apps/${SERVICE_DIR}/package.json ./apps/${SERVICE_DIR}/package.json
RUN pnpm install --frozen-lockfile --filter ./apps/${SERVICE_DIR}...

WORKDIR /app/apps/${SERVICE_DIR}
COPY ${BUILD_CONTEXT_PATH}/apps/${SERVICE_DIR}/. .

RUN pnpm build

FROM nginx:alpine

ARG SERVICE_DIR

COPY docker/web/nginx/nginx.conf /etc/nginx/nginx.conf
COPY docker/web/nginx/conf.d/ /etc/nginx/conf.d/
COPY --from=build /app/apps/${SERVICE_DIR}/dist /usr/share/nginx/html

EXPOSE 2000

CMD ["nginx", "-g", "daemon off;"]
