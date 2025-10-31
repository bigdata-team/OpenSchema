from fastapi import HTTPException, Request
from common.security.jwt_validator import get_jwt_validator


def get_gateway_auth_dependency(strict: bool = True):
    """
    Gateway 헤더 + JWT 이중 검증

    보안 레이어:
    1. Gateway에서 주입한 X-Auth-* 헤더 읽기
    2. ELPAI_JWT 쿠키에서 JWT 직접 검증 (RS256 서명 확인)
    3. 헤더와 JWT 내용 일치 확인 (불일치 시 공격으로 간주)
    4. JWT에서 한글 이름/프로필 사진 추출

    elpai-gateway는 JWT를 검증한 후 다음 헤더를 주입합니다:
    - X-Auth-Id: 사용자 ID (elpai-auth의 member.id)
    - X-Auth-Email: 이메일
    - X-Auth-Name: 이름 (한글 깨질 수 있음)
    - X-Auth-Role: 역할 (USER, ADMIN 등)
    - X-Auth-Idp-Cd: Identity Provider 코드 (GOOGLE, GITHUB 등)

    JWT 검증:
    - elpai-gateway의 JwtVerificationService.kt와 동일한 방식
    - JWK 엔드포인트에서 공개키 가져오기
    - RS256 알고리즘으로 서명 검증
    - JWT 위조 불가능 (개인키는 auth 서버만 보유)

    Args:
        strict: True면 인증 실패 시 401 에러, False면 None 반환

    Returns:
        검증된 사용자 정보 딕셔너리
        {
            "user_id": str,
            "email": str,
            "name": str,  # JWT에서 추출한 한글 이름 (정상)
            "role": str,
            "idp_cd": str,
            "picture": str | None,  # JWT에서 추출한 프로필 사진
        }

    Raises:
        HTTPException: 인증 실패 시 401 에러
            - Gateway 헤더 없음
            - JWT 쿠키 없음
            - JWT 서명 검증 실패
            - 헤더-JWT 불일치 (공격 감지)

    Example:
        @router.get("/me")
        async def get_me(
            gateway_user: dict = Depends(get_gateway_auth_dependency(strict=True))
        ):
            email = gateway_user["email"]
            name = gateway_user["name"]  # 한글 정상
            picture = gateway_user["picture"]
            # ...
    """
    async def dependency(request: Request):
        # 1. Gateway 헤더 추출
        user_id = request.headers.get("X-Auth-Id")
        email = request.headers.get("X-Auth-Email")
        name = request.headers.get("X-Auth-Name")
        role = request.headers.get("X-Auth-Role", "USER")
        idp_cd = request.headers.get("X-Auth-Idp-Cd")

        if strict and not user_id:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized - Missing authentication headers from Gateway"
            )

        # 2. JWT 쿠키 검증 (이중 검증)
        jwt_token = request.cookies.get("ELPAI_JWT")
        picture = None

        if jwt_token:
            try:
                # JWT 서명 검증 (elpai-gateway와 동일한 방식)
                jwt_validator = get_jwt_validator()
                payload = jwt_validator.validate_token(jwt_token)

                # 3. Gateway 헤더와 JWT 내용 일치 확인 (보안)
                jwt_user_id = payload.get("sub")
                jwt_email = payload.get("email")

                if user_id != jwt_user_id or email != jwt_email:
                    print(f"[Gateway Auth] Header-JWT mismatch detected!")
                    print(f"[Gateway Auth] Header: user_id={user_id}, email={email}")
                    print(f"[Gateway Auth] JWT: sub={jwt_user_id}, email={jwt_email}")
                    raise HTTPException(
                        status_code=401,
                        detail="Header-JWT mismatch - potential attack detected"
                    )

                # 4. JWT에서 한글 이름/프로필 사진 추출 (Gateway 헤더는 깨짐)
                name = payload.get("name", name)
                picture = payload.get("picture")

                print(f"[Gateway Auth] JWT validation successful for {email}")
                print(f"[Gateway Auth] Name from JWT: {name}")
                if picture:
                    print(f"[Gateway Auth] Picture from JWT: {picture}")

            except HTTPException:
                # 헤더-JWT 불일치는 그대로 raise
                raise

            except Exception as e:
                # JWT 검증 실패 → 인증 거부
                print(f"[Gateway Auth] JWT validation failed: {e}")
                if strict:
                    raise HTTPException(
                        status_code=401,
                        detail=f"JWT validation failed: {str(e)}"
                    )
        else:
            # JWT가 없으면 인증 실패
            if strict:
                raise HTTPException(
                    status_code=401,
                    detail="No JWT token found - authentication required"
                )

        # 검증된 사용자 정보 반환
        user_info = {
            "user_id": user_id,
            "email": email,
            "name": name,
            "role": role,
            "idp_cd": idp_cd,
            "picture": picture,
        }
        request.state.gateway_user = user_info

        return user_info

    return dependency
