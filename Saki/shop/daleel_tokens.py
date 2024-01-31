import jwt
from datetime import datetime, timedelta
from keys import jwt_secret

def create_token(token_type: str, access_token: str, refresh_token: str):
    payload = dict(    # **add expiru time to the token**
        token_type=token_type,
        access_token=access_token,
        refresh_token=refresh_token
    )
    token = jwt.encode(payload=payload, key=jwt_secret, algorithm="HS256")
    return token

def daleel_token(request):
    token = jwt.decode(request.COOKIES.get('daleeljwt'), key=jwt_secret, algorithms=["HS256"])
    
    return token