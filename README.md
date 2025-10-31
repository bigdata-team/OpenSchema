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

### JWT token 

#### Auth flow
```
  ─────────────────────────────────
   elpai-auth                      
   JWT 발급 & 공개키 제공              
                                    
   Keys: private.pem (서명 생성)    
         public.pem  (검증용)        
  ─────────────────────────────────
              │
              │ JWT 발급
              ▼
  ─────────────────────────────────
   브라우저                         
   Cookie: ELPAI_JWT               
  ─────────────────────────────────
              │
              │ 요청 (JWT 포함)
              ▼
  ─────────────────────────────────
   elpai-gateway                   
   [1차 검증]                        
                                   
   ✓ JWT 서명 검증 (RS256)           
   ✓ 만료시간 검증                    
   ✓ X-Auth-* 헤더 주입            
  ─────────────────────────────────
              │
              │ 헤더 + JWT
              ▼
  ─────────────────────────────────
   OpenSchema Backend              
   [2차 검증]           
                                    
   ✓ JWT 재검증 (RS256)            
   ✓ 헤더-JWT 일치 확인            
   ✓ Gateway 우회 공격 차단        
   ✓ 한글 이름 복원                
  ─────────────────────────────────
              │
              ▼
  ─────────────────────────────────
   PostgreSQL (사용자 정보)           
  ─────────────────────────────────
```

#### Architecture(OpenRouter 통합) 
```
├── elpai-auth/                              # 인증 서버
  │   └── src/main/resources/keys/
  │       └── key-YYYYMMDD-HHMMSS/
  │           ├── private.pem                   # JWT 서명 생성 (비공개)
  │           └── public.pem                    # JWT 검증 (공개)
  │
  ├── elpai-gateway/                            # API Gateway
  │   └── src/main/kotlin/.../filter/
  │       └── JwtAuthenticationGatewayFilterFactory.kt  # 1차 JWT 검증
  │
  └── OpenSchema/                               # 백엔드
      ├── src/common/
      │   ├── security/
      │   │   └── jwt_validator.py             # JWT 검증 로직 (RS256)
      │   └── dependencies/
      │       └── gateway_auth.py              # 2차 검증 + 헤더 비교
      │
      └── src/service/auth/
          └── router/public/
              └── public.py                     # /me API (사용자 정보)
```
#### JWT Endpoint
```
http://host.docker.internal:8080/api/oauth2/.well-known/jwks.json
```