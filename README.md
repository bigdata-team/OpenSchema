# OpenSchema
An experimental project for transplanting structured knowledge frameworks.

```
docker compose --env-file .env.dev -f docker-compose-kafka.yaml up
docker compose --env-file .env.dev -f docker-compose-infra.yaml up
docker compose --env-file .env.dev -f docker-compose-service.yaml up
```

```
npm run dev
```

## ui library
### shadcn
```
https://ui.shadcn.com/
```
### tailwindcss
```
https://ui.shadcn.com/docs/tailwind-v4
```


## auth 
+ local 기준 
+ ELPAI-OpenRouter의 로그인 및 인증을 사용
  + jwt 토큰 인증을 위해 gateway 사용
  + sso는 .elpai.org 도메인 cookie를 사용 
### Virtual Domain
```
127.0.0.1       openschema-local-api.elpai.org
127.0.0.1       openschema-local-ui.elpai.org
127.0.0.1       auth-local.elpai.org
127.0.0.1       gateway-local.elpai.org
```

### ELPAI-OpenRouter Auth & Gateway
```
git clone https://github.com/ELPAI-OpenRouter/elpai-auth
git clone https://github.com/ELPAI-OpenRouter/elpai-gateway.git

각각 실행
./gradlew bootRun
```

### Auth UI
```
로그인 선택 가능 페이지(버튼을 통한 로그인)
http://openschema-local-ui.elpai.org/ui/v1/auth
로그인 필수 페이지(미 로그인시 로그인 페이지로 이동)
http://openschema-local-ui.elpai.org/ui/v1/auth/protected
```

### ENV
```
VITE_API_GATEWAY_URL=http://openschema-local-api.elpai.org
VITE_UI_GATEWAY_URL=http://openschema-local-ui.elpai.org
```

