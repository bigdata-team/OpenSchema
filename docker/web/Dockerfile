FROM node:22-alpine AS build

ARG VITE_API_GATEWAY_URL
ARG VITE_AUTH_GATEWAY_URL
ARG VITE_UI_GATEWAY_URL
ARG VITE_AUTH_URL

ENV VITE_API_GATEWAY_URL=${VITE_API_GATEWAY_URL}
ENV VITE_AUTH_GATEWAY_URL=${VITE_AUTH_GATEWAY_URL}
ENV VITE_UI_GATEWAY_URL=${VITE_UI_GATEWAY_URL}
ENV VITE_AUTH_URL=${VITE_AUTH_URL}

ARG BUILD_CONTEXT_PATH=src/web
ARG SERVICE_DIR

RUN corepack enable

WORKDIR /app
COPY pnpm-workspace.yaml package.json pnpm-lock.yaml ./
# for common
COPY ${BUILD_CONTEXT_PATH}/common/ ./${BUILD_CONTEXT_PATH}/common/
RUN pnpm install --frozen-lockfile --filter "./${BUILD_CONTEXT_PATH}/common/*"
# for service
COPY ${BUILD_CONTEXT_PATH}/apps/${SERVICE_DIR}/package.json ./${BUILD_CONTEXT_PATH}/apps/${SERVICE_DIR}/package.json
RUN pnpm install --frozen-lockfile --filter ./${BUILD_CONTEXT_PATH}/apps/${SERVICE_DIR}...

WORKDIR /app/${BUILD_CONTEXT_PATH}/apps/${SERVICE_DIR}
COPY ${BUILD_CONTEXT_PATH}/apps/${SERVICE_DIR}/. .
RUN pnpm build

FROM nginx:alpine

ARG SERVICE_DIR
ARG BUILD_CONTEXT_PATH=src/web

COPY docker/web/nginx/nginx.conf /etc/nginx/nginx.conf
COPY docker/web/nginx/conf.d/ /etc/nginx/conf.d/
COPY docker/web/nginx_entrypoint.sh /nginx_entrypoint.sh
RUN chmod +x /nginx_entrypoint.sh
COPY --from=build /app/${BUILD_CONTEXT_PATH}/apps/${SERVICE_DIR}/dist /usr/share/nginx/html

EXPOSE 2000

# CMD ["nginx", "-g", "daemon off;"]
CMD ["/nginx_entrypoint.sh"]
