from pydantic import BaseModel


class SignInRequest(BaseModel):
    email: str
    password: str


class SignInResponse(BaseModel):
    access_token: str
    refresh_token: str
