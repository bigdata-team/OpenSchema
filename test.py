from common.jwt import *
from common.jwt.model import AccessTokenPayload, RefreshTokenPayload, TokenPayload

payload = AccessTokenPayload(
    iss="auth.service",
    aud="service",
    sub="user123",
    sid="session123",
    iat=1700000000,
    exp=2700003600,
    nbf=1700000000,
    jti="jwtid123",
)

v = encode(payload)
v = verify_token(v)
print(v)
