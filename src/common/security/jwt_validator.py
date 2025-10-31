"""
JWT Validation Service for OpenSchema

elpai-auth의 JWT 토큰을 검증하는 서비스입니다.
elpai-gateway의 JwtVerificationService.kt와 동일한 방식으로 동작합니다.

작동 방식:
1. JWT에서 kid (Key ID) 추출
2. JWK 엔드포인트에서 해당 kid의 공개키 가져오기
3. RS256 알고리즘으로 서명 검증
4. issuer, exp, nbf 검증
5. claims 추출

보안:
- RS256 비대칭 암호화 (개인키로 서명, 공개키로 검증)
- JWT 위조 불가능 (개인키는 auth 서버만 보유)
- JWK 공개키 24시간 캐싱 (elpai-gateway와 동일)
"""

from jwt import PyJWKClient, decode, ExpiredSignatureError, InvalidSignatureError, InvalidIssuerError
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class JwtValidator:
    """
    elpai-auth JWT 검증 클래스

    elpai-gateway의 JwtVerificationService.kt와 동일한 방식으로
    JWK(JSON Web Key) 기반 RS256 서명 검증을 수행합니다.
    """

    def __init__(self, auth_url: str = "http://host.docker.internal:8080"):
        """
        JwtValidator 초기화

        Args:
            auth_url: elpai-auth 서버 URL
                     - Docker 환경: http://host.docker.internal:8080
                     - 로컬 환경: http://openschema-local-ui.elpai.org:8080
        """
        self.auth_url = auth_url
        self.expected_issuer = "elpai-auth"

        # JWK Client 초기화
        # PyJWT 라이브러리의 내장 캐싱 사용 (자동으로 공개키 캐싱)
        self.jwks_client = PyJWKClient(
            f"{auth_url}/api/oauth2/.well-known/jwks.json",
            cache_keys=True  # 공개키 캐싱 활성화 (PyJWT 기본 캐싱 사용)
        )

        logger.info(f"JwtValidator initialized with auth server: {auth_url}")

    def validate_token(self, token: str) -> Dict:
        """
        JWT 토큰 서명 검증 및 claims 추출

        검증 과정:
        1. JWT 헤더에서 kid (Key ID) 추출
        2. JWK 엔드포인트에서 공개키 가져오기 (캐시 우선 사용)
        3. RS256 알고리즘으로 서명 검증
        4. issuer 검증 ("elpai-auth")
        5. exp (만료시간) 검증
        6. nbf (유효시작시간) 검증
        7. claims 추출

        Args:
            token: JWT 토큰 문자열

        Returns:
            검증된 JWT claims 딕셔너리
            {
                "sub": "사용자 ID",
                "email": "이메일",
                "name": "이름 (한글 정상)",
                "role": "역할",
                "idp_cd": "인증 제공자",
                "picture": "프로필 사진 URL",
                "iss": "elpai-auth",
                "exp": 만료시간,
                "iat": 발급시간,
                ...
            }

        Raises:
            Exception: JWT 검증 실패
                - "Token expired": 토큰 만료
                - "Invalid signature - token may be forged": 서명 검증 실패 (위조 의심)
                - "Invalid issuer": 발급자 불일치
                - "JWT validation failed": 기타 검증 오류
        """
        try:
            # 1. JWT 헤더에서 kid 추출 후 JWK에서 공개키 가져오기
            # elpai-gateway의 jwkProvider.get(keyId)와 동일
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)

            # 2. RS256 알고리즘으로 서명 검증 + issuer/exp/nbf 확인
            # elpai-gateway의 verifier.verify(token)와 동일
            payload = decode(
                token,
                signing_key.key,
                algorithms=["RS256"],            # elpai-auth는 RS256만 사용
                issuer=self.expected_issuer,     # "elpai-auth"
                options={
                    "verify_exp": True,          # 만료 시간 확인
                    "verify_nbf": True,          # 유효 시작 시간 확인
                    "verify_signature": True,    # 서명 검증
                    "verify_aud": False,         # audience 검증 비활성화 (JWT에 aud 없음)
                }
            )

            logger.debug(f"Successfully validated token for user: {payload.get('sub')}")

            return payload

        except ExpiredSignatureError:
            logger.warning("Token expired")
            raise Exception("Token expired")

        except InvalidSignatureError:
            logger.error("Invalid signature - token may be forged")
            raise Exception("Invalid signature - token may be forged")

        except InvalidIssuerError:
            logger.error(f"Invalid issuer - expected {self.expected_issuer}")
            raise Exception(f"Invalid issuer - expected {self.expected_issuer}")

        except Exception as e:
            logger.error(f"JWT validation failed: {str(e)}")
            raise Exception(f"JWT validation failed: {str(e)}")


# 싱글톤 인스턴스 (앱 시작 시 한 번만 생성, elpai-gateway와 동일)
_jwt_validator: Optional[JwtValidator] = None


def get_jwt_validator(auth_url: str = "http://host.docker.internal:8080") -> JwtValidator:
    """
    JwtValidator 싱글톤 인스턴스 반환

    Args:
        auth_url: elpai-auth 서버 URL (최초 생성 시에만 사용)

    Returns:
        JwtValidator 인스턴스
    """
    global _jwt_validator
    if _jwt_validator is None:
        _jwt_validator = JwtValidator(auth_url)
    return _jwt_validator
