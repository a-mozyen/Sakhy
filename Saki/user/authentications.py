from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from datetime import timedelta, datetime
from keys import access_token_key, refresh_token_key
import jwt
from Saki.variables import access_token_expiry, refresh_token_expiry


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.headers.get("access_token")
            return token
        except:
            return Exception("Unauthorized")
        
        # try:
        #     token = request.COOKIES.get("jwt")

        #     if not token:
        #         return None

        #     payload = jwt.decode(token, key=access_token_key, algorithms=["HS256"])
        #     user = User.objects.get(id=payload["id"])

        # except:
        #     raise AuthenticationFailed("Unauthorized")

        # return (user, None)


def create_token(id: int, username: str, phone: str):
    payload = dict(
        id=id,
        username=username,
        phone=phone,
        exp=access_token_expiry,
        iat=datetime.utcnow(),
    )
    token = jwt.encode(payload=payload, key=access_token_key, algorithm="HS256")
    return token

def create_refresh_token(id: int, username: str, phone: str):
    payload = dict(
        id=id,
        username=username,
        phone=phone,
        exp=refresh_token_expiry,
        iat=datetime.utcnow(),
    )
    refresh_token = jwt.encode(payload=payload, key=refresh_token_key, algorithm="HS256")
    return refresh_token