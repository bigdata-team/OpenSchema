from fastapi import HTTPException, Request
import httpx
import asyncio


def get_gateway_auth_dependency(strict: bool = True):
    """
    Gateway에서 주입한 X-Auth-* 헤더를 검증하고 사용자 정보 추출

    elpai-gateway는 JWT를 검증한 후 다음 헤더를 주입합니다:
    - X-Auth-Id: 사용자 ID (elpai-auth의 member.id)
    - X-Auth-Email: 이메일
    - X-Auth-Name: 이름
    - X-Auth-Role: 역할 (USER, ADMIN 등)
    - X-Auth-Idp-Cd: Identity Provider 코드 (GOOGLE, GITHUB 등)

    Args:
        strict: True면 헤더 없을 때 401 에러, False면 None 반환

    Returns:
        Gateway에서 추출한 사용자 정보 딕셔너리
        {
            "user_id": str,
            "email": str,
            "name": str,
            "role": str,
            "idp_cd": str,
        }

    Raises:
        HTTPException: strict=True이고 인증 헤더가 없을 때 401 에러

    Example:
        @router.get("/me")
        async def get_me(
            gateway_user: dict = Depends(get_gateway_auth_dependency(strict=True))
        ):
            email = gateway_user["email"]
            # ...
    """
    async def dependency(request: Request):
        # Gateway 헤더 추출
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

        # Gateway 헤더의 한글이 깨졌을 경우 SDK API로 정확한 정보 가져오기
        jwt_cookie = request.cookies.get("ELPAI_JWT")
        if jwt_cookie and name and "?" in name:  # 한글이 깨진 경우
            try:
                # host.docker.internal 사용 (Mac/Windows에서 호스트 접근)
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        "http://host.docker.internal:8080/api/oauth2/userinfo",
                        cookies={"ELPAI_JWT": jwt_cookie},
                        timeout=5.0
                    )

                    if response.status_code == 200:
                        sdk_data = response.json()
                        # SDK에서 정상적인 한글 이름 가져오기
                        name = sdk_data.get("name", name)
                        print(f"[Gateway Auth] Successfully fetched name from SDK: {name}")
            except Exception as e:
                print(f"[Gateway Auth] Failed to fetch from SDK: {e}, using Gateway data")

        # request.state에 저장 (다른 곳에서도 접근 가능)
        user_info = {
            "user_id": user_id,
            "email": email,
            "name": name,
            "role": role,
            "idp_cd": idp_cd,
        }
        request.state.gateway_user = user_info

        return user_info

    return dependency
