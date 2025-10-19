#####################################################################
# build stage
FROM node:22.18.0-alpine AS build-stage

ARG BUILD_CONTEXT_PATH=src/web
ARG SERVICE_DIR
ARG VITE_SERVICE_TYPE
ARG VITE_SERVICE_NAME
ARG VITE_SERVICE_VERSION
ARG UI_DEPENDENCY_AUTH
ARG UI_DEPENDENCY_CHAT

RUN corepack enable

WORKDIR /app
COPY ${BUILD_CONTEXT_PATH}/pnpm-workspace.yaml ${BUILD_CONTEXT_PATH}/package.json ${BUILD_CONTEXT_PATH}/pnpm-lock.yaml ./
COPY ${BUILD_CONTEXT_PATH}/apps/${SERVICE_DIR}/package.json ./apps/${SERVICE_DIR}/package.json
RUN pnpm install --frozen-lockfile --filter ./apps/${SERVICE_DIR}...


WORKDIR /app/apps/${SERVICE_DIR}
COPY ${BUILD_CONTEXT_PATH}/apps/${SERVICE_DIR}/. .
RUN pnpm build

#####################################################################
# production stage
FROM nginx:1.29.2-alpine AS production-stage

ARG SERVICE_DIR

COPY docker/web/nginx.conf /etc/nginx/
COPY docker/web/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/apps/${SERVICE_DIR}/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
