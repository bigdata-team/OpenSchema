from fastapi import APIRouter, Depends, Request
from model.http.signin import SignInRequest, SignInResponse
from model.http.signup import SignUpRequest
from model.sql import User
from service.signin import SignInService
from service.signup import SignUpService
from repository.sql.user import UserRepository

from common.model.http import Body, DataBody, create_response
from common.dependencies import get_gateway_auth_dependency

router = APIRouter(tags=["public"])


@router.get("/ping", response_model=Body)
async def ping():
    return create_response(detail="pong")


@router.post("/signup", response_model=DataBody[User])
async def signup(body: SignUpRequest, service: SignUpService = Depends(SignUpService)):
    return await service.signup(body.email, body.password)


@router.post("/signin", response_model=DataBody[SignInResponse])
async def signin(body: SignInRequest, service: SignInService = Depends(SignInService)):
    return await service.signin(body.email, body.password)


@router.get("/me", response_model=DataBody[User])
async def get_me(
    request: Request,
    gateway_user: dict = Depends(get_gateway_auth_dependency(strict=True)),
    repo: UserRepository = Depends(UserRepository),
):
    """
    현재 로그인한 사용자 정보 조회

    Gateway에서 주입한 X-Auth-* 헤더를 통해 사용자 인증.
    첫 로그인 시 자동으로 사용자 계정 생성 (SSO auto-provisioning).

    Flow:
    1. Gateway 헤더에서 이메일 추출
    2. DB에서 이메일로 사용자 조회
    3. 없으면 새 사용자 생성 (idp_cd, hashed_password=None)
    4. 사용자 정보 반환

    Returns:
        현재 로그인한 사용자 정보
    """
    email = gateway_user["email"]

    # 1. 이메일로 기존 사용자 찾기
    user = await repo.get_by_email(email)

    # gateway_auth.py에서 이미 JWT 검증 및 데이터 추출 완료
    # - JWT 서명 검증 완료 (RS256)
    # - 헤더-JWT 일치 확인 완료
    # - 한글 이름 복원 완료
    # - 프로필 사진 추출 완료
    name = gateway_user["name"]      # JWT에서 추출한 정상 한글
    role = gateway_user.get("role")
    picture = gateway_user.get("picture")  # JWT에서 추출한 프로필 사진

    # 2. 기존 사용자가 있고 정보가 변경되었으면 업데이트
    if user:
        updated = False
        if user.name != name:
            user.name = name
            updated = True
        if user.picture != picture:
            user.picture = picture
            updated = True
        if role and user.role != role:
            user.role = role
            updated = True

        if updated:
            user = await repo.update(user.id, user)  # id와 객체 모두 전달

    # 3. 없으면 자동 생성 (첫 SSO 로그인)
    if not user:
        user = User(
            email=email,
            name=name,
            role=role,
            idp_cd=gateway_user["idp_cd"],
            hashed_password=None,  # SSO 사용자는 비밀번호 없음
            picture=picture,  # SDK에서 가져온 프로필 이미지
            bio=None,
        )
        user = await repo.create(user)

    return create_response(data=user)
