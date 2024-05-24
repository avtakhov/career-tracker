import datetime

import fastapi
from sqladmin.authentication import AuthenticationBackend
from jose import jwt

from app.settings import settings


def check_authorization(api_key: str = fastapi.Header(None)):
    if api_key != settings.api_key:
        raise fastapi.HTTPException(status_code=401, detail="Unauthorized")

    return api_key


def create_jwt_token(data: dict, expiration_delta: datetime.timedelta) -> str:
    expiration = datetime.datetime.utcnow() + expiration_delta
    data.update({"exp": expiration})
    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)


def create_access_token(username: str) -> str:
    return create_jwt_token(
        {"scopes": "access_token", "username": username},
        datetime.timedelta(weeks=8),
    )


def get_username(token) -> str | None:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        return payload.get("username")
    except (jwt.ExpiredSignatureError, jwt.JWTError):
        return None


class AdminAuth(AuthenticationBackend):
    async def login(self, request: fastapi.Request) -> bool:
        form = await request.form()
        print(form)
        password = form["password"]

        if password != settings.admin_pass:
            return False

        # And update session
        token = create_access_token(form.get("username"))
        request.session.update({"token": token})

        return True

    async def logout(self, request: fastapi.Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: fastapi.Request):
        token = request.session.get("token")

        if not token or (username := get_username(token)) is None:
            return fastapi.responses.RedirectResponse(
                request.url_for("admin:login"), status_code=302
            )

        request.session.update({"username": username})
