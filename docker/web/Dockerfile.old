#####################################################################
# build stage
FROM node:22.18.0-alpine AS build-stage

ARG SERVICE_DIR
ARG VITE_APP_OPENSCHEMA_UI_URL

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

ENV VITE_APP_OPENSCHEMA_UI_URL=${VITE_APP_OPENSCHEMA_UI_URL}

WORKDIR /app
COPY docker/web/nginx.conf ./
COPY docker/web/default.conf ./
COPY src/web/${SERVICE_DIR}/package.json src/web/${SERVICE_DIR}/pnpm-lock.yaml ./
# RUN pnpm install --frozen-lockfile
RUN pnpm install
COPY src/web/${SERVICE_DIR}/. .
RUN pnpm build

#####################################################################
# production stage
FROM nginx:1.29.2-alpine AS production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY --from=build-stage /app/nginx.conf /etc/nginx/
COPY --from=build-stage /app/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
