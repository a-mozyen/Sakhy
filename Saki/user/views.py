from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from .authentications import CustomAuthentication, create_token
from .serializers import UserSerializer
from .models import User, Otp
from random import randint
from keys import unifonic_key
import requests


class Register(APIView):
    '''
    Required fields {"username": "<str: your username>", "phone": "<str: your phone number>", "country_code": "<str: your country code>"}
    Note: phone number is a 9 digit without '0' at the beginning .ex (504XXXXXX).
          Enter country code with '+' .ex(+966), default is (+966).
    '''
    def post(self, request):
        user = UserSerializer(data=request.data)
        if user.is_valid(raise_exception=True):
            user.save()
            return Response(data="User created", status=status.HTTP_201_CREATED)
        else:
            raise APIException(detail=user.errors)


class Login(APIView):
    '''
    field {"phone": "<str: your phone number>"}
    Take the phone number and send an otp code to the given phone number.
    phone number is a 9 digit without '0' at the beginning .ex (504XXXXXX).
    '''
    def post(self, request):
        phone = request.data.get('phone')
        try:
            user = User.objects.get(phone=phone)
        except:
            raise APIException(detail='Phone number not registered!')
        
        code = user.country_code.lstrip('+')
        phone = code+phone
        otp = randint(1000, 9999)

        Otp.objects.create(
            user=user,
            code=otp,
            expirey=timezone.now()+timezone.timedelta(minutes=5),
            utilized=False
        )
        
        # sending a request to unufonic api.
        url = 'https://el.cloud.unifonic.com/rest/SMS/messages'
        param = {
            "AppSid": unifonic_key,
            "Recipient": phone,
            "Body": f"Your login code {otp}"
        }
        
        response = requests.post(url=url, data=param)
        data = response.json()
        
        with open('D:\github\Saki\Saki\OTP_log.txt', 'w') as log:
            log.write(f'user:{user.username} log:{data}')
        
        return Response(data=f'OTP code sent to {phone}', status=status.HTTP_200_OK)
    

class Verify_Otp(APIView):
    '''
    field {"code": <int: received code>}
    Verify the entered otp code to the generated code. Then, generate token.
    '''
    def post(self, request):
        try:
            otp_code = request.data.get('code')
            otp_data = Otp.objects.get(code=otp_code)
            user = User.objects.get(username=otp_data.user)
        except:
            raise APIException(detail='Wrong code')
        
        if otp_data.utilized == False:
            if timezone.now() < otp_data.expirey:
                token = create_token(id=user.id, username=user.username, phone=user.phone)
                responce = Response(data="Login successfull", status=status.HTTP_200_OK)
                responce.set_cookie(key="jwt", value=token, httponly=True)
                otp_data.utilized = True
                otp_data.save()
                return responce
            else:
                return Response(data='Expired OTP code')
        else:
            return Response(data='OTP code been used before')
        
    # def post(self, request):
    #     try:
    #         email = request.data.get("email")
    #         email = email.lower()
    #         user = User.objects.get(email=email)
    #     except:
    #         raise APIException(detail="Wrong credentials")

    #     try:
    #         password = request.data.get("password")
    #         check_password(password=password, encoded=user.password)
    #     except:
    #         raise APIException(detail="Wrong credentials")

    #     token = create_token(id=user.id, username=user.username, email=user.email)
    #     responce = Response(data="Login successfull", status=status.HTTP_200_OK)
    #     responce.set_cookie(key="jwt", value=token, httponly=True)
    #     return responce


class UserProfile(APIView):
    authentication_classes = [
        CustomAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = User.objects.get(id=request.user.id)
        data = request.data
        serializer = UserSerializer(instance=user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data="Successfully updated", status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = User.objects.get(id=request.user.id)
        user.delete()
        response = Response(data="User deleted", status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("jwt")
        return response


class Logout(APIView):
    '''
    Take no data. 
    When post sent, token is deleted.
    '''
    authentication_classes = [
        CustomAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        responce = Response(data="Logout Successfull", status=status.HTTP_200_OK)
        responce.delete_cookie("jwt")
        return responce
