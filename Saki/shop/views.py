from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from .serializers import (StoreSerializer, CouponSerializer, OrderSerializer, 
                          AddStoreSerializer, AddCouponSerializer)
from user.serializers import UserSerializer
from .models import Store, Coupon, Order
from user.models import User
from user.authentications import CustomAuthentication
from rest_framework.permissions import IsAuthenticated
import requests
import json


class GetToken(APIView):
    def get(self, request):
        endpoint = "https://daleelapi.com/api/v1/oauth/token"

        payload = {
            'grant_type': 'password',
            'client_id': '2',
            'client_secret': 'D1uvg3aUd79fDIvqduYlaV3q1b59XztrPPooADyDrIo=',
            'username': 'merchants.api@daleelstore.com',
            'password': 'ABC12345'
            }
        
        header = {
        'Content-Type': 'application/json'
        }

        response = requests.post(
            url="https://daleelapi.com/api/v1/oauth/token", 
            params= None,
            headers={'Content-Type': 'application/json'}, 
            data={
            'grant_type': 'password',
            'client_id': '2',
            'client_secret': 'D1uvg3aUd79fDIvqduYlaV3q1b59XztrPPooADyDrIo=',
            'username': 'merchants.api@daleelstore.com',
            'password': 'ABC12345'
            },
            auth= None,
            allow_redirects= True
            )
        token = response.json()
        
        return Response(data=token)
    
    # curl -X POST "https://daleelapi.com/api/v1/oauth/token" -H "Content-Type: application/json" -d '{"grant_type": "password", "client_id": "2", "client_secret": "D1uvg3aUd79fDIvqduYlaV3q1b59XztrPPooADyDrIo=", "username": "merchants.api@daleelstore.com", "password": "ABC12345"}'
    

class RefreshToken(APIView):
    def refresh_token():
        url = "https://daleelapi.com/api/v1/oauth/token"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'token eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjI4NWQyYWZhYzcyYzNkYTU2NTg5MWUwMTIzMmE5Y2U1ZTU2Yjc0M2Y0OTRmZTU5ZjA0MzJjOWZjMzA1Yzk0ZDExNDI1M2VkZTZkZjMzNDVlIn0.eyJhdWQiOiIyIiwianRpIjoiMjg1ZDJhZmFjNzJjM2RhNTY1ODkxZTAxMjMyYTljZTVlNTZiNzQzZjQ5NGZlNTlmMDQzMmM5ZmMzMDVjOTRkMTE0MjUzZWRlNmRmMzM0NWUiLCJpYXQiOjE2NTQxNjI1ODMsIm5iZiI6MTY1NDE2MjU4MywiZXhwIjoxNjg1Njk4NTgzLCJzdWIiOiIiLCJzY29wZXMiOlsiKiJdfQ.E-ikupArlD7LRFD-j6z-1drWXJedwG9_Bo9LbFOpMPjFyVprOMiQ9F9XnsXfTEiBmVbUjl2wSzYtPuKjbndYkU8JvfVNASP-UAuE44l8OkyB1E10UabXyc2kgEMGDe6DtYbBULE5kX8sStnNLdwHGR1iknlXlT4TW9NFFto6w0KIg_T9XlCmrZrFHsP35dlbTRl229L5WCQmIexnU4U6a8UWBSKCjjeD673e3iEzK_FkTDdrgTyVb_G_85sUIFElPdCjSbqKDYmW9L02bOpeAwjDLSB7qv0W3rLbthEaGx0SHFwUYjjr23ygfdwTp6BUlte_iekezQKYAeMgS7LixEFW0anUPhlHsLcfvn5H8bka4wVkarXERw_2FQU7-5x2Flrw3trijU7L2EVKhNgcWnicWDT-YarWiAnhIEzjMQ8H4iTNHivsL69L9h2PVwvdF3Bdm28M8UsPNLQAsiAlNiXlvcRTIsYh2l7ssiUV_Xg8PEGfjw7Fu22se0haBnbOwXC6bYssWM6awLZKankEbqNqSOlK6unhVuCJ2UOVKDcE0fUQe0muuVnUaywuHHYrT_BNecxsMTtBLl6JbBNbvnYco4Mswzx7ZJHroRJnbwCUrN9QrmhN7cdh8H52I5yNg_g_bBjaOr4dLuM0Xpp81YjfVOlMfqZgqEHkfEP9f0Y'
        }
        
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": "def502003b79eaa3258d026020e46cb83f9ee08059766277e21530ad76e30881a6c5d034d34d1c6b653cc588953776f70d1bbbc2a0acb0582d86600ed00dfb2d057efeca87744464ed063710f7ee416e5a1727ba936a7f59c3adb5975cd6bc0b2a7958910b330b2d58b0c306cd5f756704a66edb7ce025d71278b7b8cd73348857526089e326fb7711c3082069de9a3a5bee4be7da0e41575ad88b3f7f29984fdc962137a3064026765a7ac13a4b9cf461da8ba4c8c9d633c72a6a3eb7a509fc900fc729085c745f3783a2b1150dec9707fa00dcea7918ba4ea1f4a65498eb3bd56719f85a5eed7418b3456712fb917cf9cbcd881a4933b5e54927c1cc9fc8996b2491ecae5396326524f53b94172879cb8affe07802c413400b3b9deedb2af597aad5ec432aa70d6c8a81aa65c492812758ab3a97e4e8510ad03cf35b854eb3c6bf646e17a4ceea7de8c7b78ebb00f08976fe65fe8999231ee19d9c18dff75dfce89ae285",
            "client_id": "2",
            "client_secret": "D1uvg3aUd79fDIvqduYlaV3q1b59XztrPPooADyDrIo="
        }
        
        response = requests.post(url=url, headers=headers, data=payload)
        token = response.json()
        
        return token


class ListAllItems(APIView):
    def post(self, request):
        url = "https://daleelapi.com/api/v1/get_items"

        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'token eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6Ijg3YTZhNjVjMzVhMWM0Y2U2NzI3MDY4ZTVmNWJmYTYzODc0ZWFlNWM0ZTU2OTNiMmM4MDcwMzEzOWM4NzQxMzk2MWNhYmExOWQwMDZiNzExIn0.eyJhdWQiOiIyIiwianRpIjoiODdhNmE2NWMzNWExYzRjZTY3MjcwNjhlNWY1YmZhNjM4NzRlYWU1YzRlNTY5M2IyYzgwNzAzMTM5Yzg3NDEzOTYxY2FiYTE5ZDAwNmI3MTEiLCJpYXQiOjE2Nzg5Njg1MjcsIm5iZiI6MTY3ODk2ODUyNywiZXhwIjoxNzEwNTkwOTI3LCJzdWIiOiIiLCJzY29wZXMiOlsiKiJdfQ.K4RY0pTftFllSLFS-x2P6Fc8A7RvhGZ4kU62kPs-1i_rG8KkURvbLVO6LyQNFhFeYSUgvtR5ShjNogdEeTFIYUJFAgTO7MLetEeS48gR9dxANOt3-r9YmiGAE8U0zhXnrpwiWDH6OBU0yFJ3B3q6Dk42GPhDbA9g-kfFkPdw2QNeptOaNAWq68ZbOMlMsXf6s12KIYaIRqvMIAB56IE5lRo737JLrkArYqXLPQxMGhKWysIU35LuqTNx52CqE7cx6eiAgHvPiXHqaYUfGTnaPa-vtVWgWAS2RwCUoZvLABrTrniTZ96KBNdOSh7fHwfiferlfa72wqMDTx8vKgzXQcaAwr2_g9_TXVlRLdIxjgmFqkgNM61uxAmsMv7omcGMK6zP4-DCzwCKnopSz0sDW2FdLDRycJgAY2Sz0RyvWoA9dfM4pLJRdvXd755uR_T4uL7bOvVHpOFQnKtYhgrF8gyxhimxBoRlLZ_7knypD8EkS6qjfTWrLl9TxE1WuqOjH4dbC_Cy3F6F511rsv7joPhfNfkBL4noUVysYiqVAg6F2w7Zahsf5zKe_gymCjG5EbUchdPi1HDXFkUSqXxGXOxDYBtqCY8fI6PxHXxA9ekHDsyHAU62q0XQien5apWFEwE8fmNMx4ACdMDCbCTBLLz8bLNOHS2lObmQNbfVoCg',
        'lang': 'ar'
        }

        payload = {
            "category_id": "1",
            "product_id": "1",
            "store_id": "1"
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        items = response.json()

        return Response(data=items)
    

class CheckAvailablity(APIView):
    def post(self, request):
        url = "https://daleelapi.com/api/v1/check_item"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'token eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6Ijg3YTZhNjVjMzVhMWM0Y2U2NzI3MDY4ZTVmNWJmYTYzODc0ZWFlNWM0ZTU2OTNiMmM4MDcwMzEzOWM4NzQxMzk2MWNhYmExOWQwMDZiNzExIn0.eyJhdWQiOiIyIiwianRpIjoiODdhNmE2NWMzNWExYzRjZTY3MjcwNjhlNWY1YmZhNjM4NzRlYWU1YzRlNTY5M2IyYzgwNzAzMTM5Yzg3NDEzOTYxY2FiYTE5ZDAwNmI3MTEiLCJpYXQiOjE2Nzg5Njg1MjcsIm5iZiI6MTY3ODk2ODUyNywiZXhwIjoxNzEwNTkwOTI3LCJzdWIiOiIiLCJzY29wZXMiOlsiKiJdfQ.K4RY0pTftFllSLFS-x2P6Fc8A7RvhGZ4kU62kPs-1i_rG8KkURvbLVO6LyQNFhFeYSUgvtR5ShjNogdEeTFIYUJFAgTO7MLetEeS48gR9dxANOt3-r9YmiGAE8U0zhXnrpwiWDH6OBU0yFJ3B3q6Dk42GPhDbA9g-kfFkPdw2QNeptOaNAWq68ZbOMlMsXf6s12KIYaIRqvMIAB56IE5lRo737JLrkArYqXLPQxMGhKWysIU35LuqTNx52CqE7cx6eiAgHvPiXHqaYUfGTnaPa-vtVWgWAS2RwCUoZvLABrTrniTZ96KBNdOSh7fHwfiferlfa72wqMDTx8vKgzXQcaAwr2_g9_TXVlRLdIxjgmFqkgNM61uxAmsMv7omcGMK6zP4-DCzwCKnopSz0sDW2FdLDRycJgAY2Sz0RyvWoA9dfM4pLJRdvXd755uR_T4uL7bOvVHpOFQnKtYhgrF8gyxhimxBoRlLZ_7knypD8EkS6qjfTWrLl9TxE1WuqOjH4dbC_Cy3F6F511rsv7joPhfNfkBL4noUVysYiqVAg6F2w7Zahsf5zKe_gymCjG5EbUchdPi1HDXFkUSqXxGXOxDYBtqCY8fI6PxHXxA9ekHDsyHAU62q0XQien5apWFEwE8fmNMx4ACdMDCbCTBLLz8bLNOHS2lObmQNbfVoCg'
            }
        
        payload = {
            "item_id": "31",
            "qty": "1"
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        check = response.json()
        
        return Response(data=check)
    

class CheckBalance(APIView):
    def post(self, request):
        url = "https://daleelapi.com/api/v1/get_balance"

        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'token eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6Ijg3YTZhNjVjMzVhMWM0Y2U2NzI3MDY4ZTVmNWJmYTYzODc0ZWFlNWM0ZTU2OTNiMmM4MDcwMzEzOWM4NzQxMzk2MWNhYmExOWQwMDZiNzExIn0.eyJhdWQiOiIyIiwianRpIjoiODdhNmE2NWMzNWExYzRjZTY3MjcwNjhlNWY1YmZhNjM4NzRlYWU1YzRlNTY5M2IyYzgwNzAzMTM5Yzg3NDEzOTYxY2FiYTE5ZDAwNmI3MTEiLCJpYXQiOjE2Nzg5Njg1MjcsIm5iZiI6MTY3ODk2ODUyNywiZXhwIjoxNzEwNTkwOTI3LCJzdWIiOiIiLCJzY29wZXMiOlsiKiJdfQ.K4RY0pTftFllSLFS-x2P6Fc8A7RvhGZ4kU62kPs-1i_rG8KkURvbLVO6LyQNFhFeYSUgvtR5ShjNogdEeTFIYUJFAgTO7MLetEeS48gR9dxANOt3-r9YmiGAE8U0zhXnrpwiWDH6OBU0yFJ3B3q6Dk42GPhDbA9g-kfFkPdw2QNeptOaNAWq68ZbOMlMsXf6s12KIYaIRqvMIAB56IE5lRo737JLrkArYqXLPQxMGhKWysIU35LuqTNx52CqE7cx6eiAgHvPiXHqaYUfGTnaPa-vtVWgWAS2RwCUoZvLABrTrniTZ96KBNdOSh7fHwfiferlfa72wqMDTx8vKgzXQcaAwr2_g9_TXVlRLdIxjgmFqkgNM61uxAmsMv7omcGMK6zP4-DCzwCKnopSz0sDW2FdLDRycJgAY2Sz0RyvWoA9dfM4pLJRdvXd755uR_T4uL7bOvVHpOFQnKtYhgrF8gyxhimxBoRlLZ_7knypD8EkS6qjfTWrLl9TxE1WuqOjH4dbC_Cy3F6F511rsv7joPhfNfkBL4noUVysYiqVAg6F2w7Zahsf5zKe_gymCjG5EbUchdPi1HDXFkUSqXxGXOxDYBtqCY8fI6PxHXxA9ekHDsyHAU62q0XQien5apWFEwE8fmNMx4ACdMDCbCTBLLz8bLNOHS2lObmQNbfVoCg'
        }

        payload = {}

        response = requests.request("POST", url, headers=headers, data=payload)
        balance = response.json()

        return Response(data=balance)
    

class Purchase(APIView):
    def post(self, request):
        url = "https://daleelapi.com/api/v1/purchase"

        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjU1MmIyNjY4ODZiZWUyODFlMzNlMTAzZTg0OWM5N2IxNTViYTE1ZmIxYzg5OGYwMTFjNDAxOGY0Y2NkZTkxZDg0OGU0NTAxZDRjYzc2YWI0In0.eyJhdWQiOiIyIiwianRpIjoiNTUyYjI2Njg4NmJlZTI4MWUzM2UxMDNlODQ5Yzk3YjE1NWJhMTVmYjFjODk4ZjAxMWM0MDE4ZjRjY2RlOTFkODQ4ZTQ1MDFkNGNjNzZhYjQiLCJpYXQiOjE1ODA0NzY1MzAsIm5iZiI6MTU4MDQ3NjUzMCwiZXhwIjoxNjEyMDk4OTMwLCJzdWIiOiI0MDQxNSIsInNjb3BlcyI6WyIqIl19.rYIe_fF0-YQJw8FXKbuy5SAeM71UWR6OMptrJjA8Y6SCx-3e0JwZkjeErTsonlE7wzRSB9ueHJMAwUceI0w_z5_LMt6rdiCxaTq0bMfmk5Be-6e9u53SUKngqYz7Uz-ucDYfmq9xbvkqB3uAzQ2TsizRLNIhf7WrlQCbW8knUNMiIStH_BRRuuZ3jgPM95_NftHI7zHtkN0XxbO_UW9JGx6HsMuXLkTtwLLflpM1o7qNwIiwXK-Mllrt_2792s5fksYJ4kb1d298KtlmsOwf5I3s-FadPygqSz02Xs6bOHeeEOb0p01wJxsQanoM2GRlwuwW47Tmrw3pqkdMwRwE6xNBmmDmbsnPbe6EopINQFOwBpmRfNE1W_GH7Ybr68e4BHRjJOYrqrIGbrENn822HFR1OjulBpMTgFnXXRVbQRdTAdnEqMeUzlTouoNPbzTZbUNFr030X0x6265xaleQ4BD1A3cFNZMwiDGwM305M645jCTVpBf7VQVMo5Ntr-Bk-rmCWOd1IzZid4uL3rRYfBgPLNcFNMQwAmJMZiFkO1rCA1kcCj1qjVD983zj_9XVyns4StDzhnVyEyoUIhs7HhTO67jyK34KthONusiFTE-_S-YxfIet-XD35xJvh-MDgIHKT2jl_wcICd29kGER_Jz-anOKsNdtGXbUpF6x3sk',
        'Authorization': 'token eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6Ijg3YTZhNjVjMzVhMWM0Y2U2NzI3MDY4ZTVmNWJmYTYzODc0ZWFlNWM0ZTU2OTNiMmM4MDcwMzEzOWM4NzQxMzk2MWNhYmExOWQwMDZiNzExIn0.eyJhdWQiOiIyIiwianRpIjoiODdhNmE2NWMzNWExYzRjZTY3MjcwNjhlNWY1YmZhNjM4NzRlYWU1YzRlNTY5M2IyYzgwNzAzMTM5Yzg3NDEzOTYxY2FiYTE5ZDAwNmI3MTEiLCJpYXQiOjE2Nzg5Njg1MjcsIm5iZiI6MTY3ODk2ODUyNywiZXhwIjoxNzEwNTkwOTI3LCJzdWIiOiIiLCJzY29wZXMiOlsiKiJdfQ.K4RY0pTftFllSLFS-x2P6Fc8A7RvhGZ4kU62kPs-1i_rG8KkURvbLVO6LyQNFhFeYSUgvtR5ShjNogdEeTFIYUJFAgTO7MLetEeS48gR9dxANOt3-r9YmiGAE8U0zhXnrpwiWDH6OBU0yFJ3B3q6Dk42GPhDbA9g-kfFkPdw2QNeptOaNAWq68ZbOMlMsXf6s12KIYaIRqvMIAB56IE5lRo737JLrkArYqXLPQxMGhKWysIU35LuqTNx52CqE7cx6eiAgHvPiXHqaYUfGTnaPa-vtVWgWAS2RwCUoZvLABrTrniTZ96KBNdOSh7fHwfiferlfa72wqMDTx8vKgzXQcaAwr2_g9_TXVlRLdIxjgmFqkgNM61uxAmsMv7omcGMK6zP4-DCzwCKnopSz0sDW2FdLDRycJgAY2Sz0RyvWoA9dfM4pLJRdvXd755uR_T4uL7bOvVHpOFQnKtYhgrF8gyxhimxBoRlLZ_7knypD8EkS6qjfTWrLl9TxE1WuqOjH4dbC_Cy3F6F511rsv7joPhfNfkBL4noUVysYiqVAg6F2w7Zahsf5zKe_gymCjG5EbUchdPi1HDXFkUSqXxGXOxDYBtqCY8fI6PxHXxA9ekHDsyHAU62q0XQien5apWFEwE8fmNMx4ACdMDCbCTBLLz8bLNOHS2lObmQNbfVoCg'
        }

        payload = {
            "item_id": "31",
            "qty": "1",
            "reference": "DS2023112"
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        purchase = response.json()

        return Response(data=purchase)

class PurchaseDetails(APIView):
    def post(self, request):
        url = "https://daleelapi.com/api/v1/purchase_details"

        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'token eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6Ijg3YTZhNjVjMzVhMWM0Y2U2NzI3MDY4ZTVmNWJmYTYzODc0ZWFlNWM0ZTU2OTNiMmM4MDcwMzEzOWM4NzQxMzk2MWNhYmExOWQwMDZiNzExIn0.eyJhdWQiOiIyIiwianRpIjoiODdhNmE2NWMzNWExYzRjZTY3MjcwNjhlNWY1YmZhNjM4NzRlYWU1YzRlNTY5M2IyYzgwNzAzMTM5Yzg3NDEzOTYxY2FiYTE5ZDAwNmI3MTEiLCJpYXQiOjE2Nzg5Njg1MjcsIm5iZiI6MTY3ODk2ODUyNywiZXhwIjoxNzEwNTkwOTI3LCJzdWIiOiIiLCJzY29wZXMiOlsiKiJdfQ.K4RY0pTftFllSLFS-x2P6Fc8A7RvhGZ4kU62kPs-1i_rG8KkURvbLVO6LyQNFhFeYSUgvtR5ShjNogdEeTFIYUJFAgTO7MLetEeS48gR9dxANOt3-r9YmiGAE8U0zhXnrpwiWDH6OBU0yFJ3B3q6Dk42GPhDbA9g-kfFkPdw2QNeptOaNAWq68ZbOMlMsXf6s12KIYaIRqvMIAB56IE5lRo737JLrkArYqXLPQxMGhKWysIU35LuqTNx52CqE7cx6eiAgHvPiXHqaYUfGTnaPa-vtVWgWAS2RwCUoZvLABrTrniTZ96KBNdOSh7fHwfiferlfa72wqMDTx8vKgzXQcaAwr2_g9_TXVlRLdIxjgmFqkgNM61uxAmsMv7omcGMK6zP4-DCzwCKnopSz0sDW2FdLDRycJgAY2Sz0RyvWoA9dfM4pLJRdvXd755uR_T4uL7bOvVHpOFQnKtYhgrF8gyxhimxBoRlLZ_7knypD8EkS6qjfTWrLl9TxE1WuqOjH4dbC_Cy3F6F511rsv7joPhfNfkBL4noUVysYiqVAg6F2w7Zahsf5zKe_gymCjG5EbUchdPi1HDXFkUSqXxGXOxDYBtqCY8fI6PxHXxA9ekHDsyHAU62q0XQien5apWFEwE8fmNMx4ACdMDCbCTBLLz8bLNOHS2lObmQNbfVoCg'
        }

        payload = {
            "purchase_id": "21304401"
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        details = response.json()

        return Response(data=details)

class AllPurchases(APIView):
    def post(self, request):
        url = "https://daleelapi.com/api/v1/all_purchase"

        headers = {
        'Authorization': 'token eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjM1ZDE3OGJkYjU5MGMzMzQyNTUwMThiODYzMmEwYzJjYThjYTEwNTU2ZWY2YjNiYjBjOWFlYjY5M2M0MjIwYWQ0MGU0Mjc2ZDI2NDBlN2NiIn0.eyJhdWQiOiIyIiwianRpIjoiMzVkMTc4YmRiNTkwYzMzNDI1NTAxOGI4NjMyYTBjMmNhOGNhMTA1NTZlZjZiM2JiMGM5YWViNjkzYzQyMjBhZDQwZTQyNzZkMjY0MGU3Y2IiLCJpYXQiOjE2Nzg5Njk3MzksIm5iZiI6MTY3ODk2OTczOSwiZXhwIjoxNzEwNTkyMTM5LCJzdWIiOiI0MDQxNSIsInNjb3BlcyI6W119.Xc9qqGGhp_GtMhBqzAMopRhgtzhV7x0Yz9AJodsNZASnNKUVH8Akj-4vo4_CBS3mwz6kffh82StbHxYU9Sv3t0wnAMDtWIIYrN78GyItgl70SVbEBNT19qbgVL3fz-Zsr7FjM_Vyq6diSPnXf4fHpLq1rmss4_Z3jRznUZfLyAMM7PbkH0M8ASYswObuy4CzZpbGSWPd86rYp2K56RE60OzV4o-pRgPXXeObryaUWdv-jw0uNpL2mNF_UUEEZF58W0_cLUu56GX3wKtY1dcHM1x_DJcXV5dbgvOy-azco2Zy6b6hiASKIku1PthzDTaQT4NKPJbk8WCpBST0sbwjanuhaDphWIk6IBn3PlhZ2AVKNuXlcP6kIEI8GHcrd8biiu2wcWWNeM2RaCTodlCKydkedOF0pnX3gxuoya6W8cRnApsKxb9huy0V1iEZWFTPYL7LVaHU2-7DcfsF6_lLtcSoyfESTasaqEe7L1GFf9WvmkzkIXSBbdInNk-dPDAEHKquAdA-_q8iEnS2GMOzsA8qe5SW7gGPRjRqE736pECVreNmmv2oKgDmbrsWMbMqqqczJxFKWMJR7_oTHJiMv73LRyo2RuIhbaTf3_0YtbrmDe67UPdUY_aUWug8hRYIr0jHYhU7ckZXDJbPNuhQbewI-zOk3o7dQRaFYWFqp6Q',
        }

        payload = json.dumps({
        "from_date": "2023-04-13 19:59",
        "to_date": "2023-04-20 15:24",
        "reference": ""
        })
        
        response = requests.request("POST", url, headers=headers, data=payload)
        


# class AddStore(APIView):
#     '''
    
#     '''
#     authentication_classes = [CustomAuthentication,]
#     permission_classes = [IsAuthenticated,]
#     def post(self, request):
#         store = AddStoreSerializer(data=request.data)

#         if store.is_valid(raise_exception=True):
#             store.save()
#             return Response(data='Store added')
#         else:
#             raise exceptions.APIException(detail=store.errors)


# class AddCoupons(APIView):
#     '''
    
#     '''
#     authentication_classes = [CustomAuthentication,]
#     permission_classes = [IsAuthenticated,]
#     def post(self, request, store_id):
#         coupon_price = request.data.get('coupon_price')
#         store = Store.objects.get(store_id=store_id)

#         if not coupon_price:
#             raise exceptions.APIException(detail='Field missing')
        
#         coupon = Coupon.objects.create(
#             store_id=store,
#             coupon_price=coupon_price
#         )
#         serializer = AddCouponSerializer(instance=coupon)
#         return Response(serializer.data)

# class StoresList(APIView):
#     '''
    
#     '''
#     def get(self, request):
#         try:
#             stores = Store.objects.all()
#             serializer = StoreSerializer(instance=stores, many=True)
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         except:
#             raise exceptions.APIException(
#                 detail=serializer.errors, code=status.HTTP_400_BAD_REQUEST
#             )


# class StoreCoupons(APIView):
#     '''
    
#     '''
#     def get(self, request, store_id):
#         try:
#             coupons = Coupon.objects.filter(store_id=store_id)
#             serializer = CouponSerializer(instance=coupons, many=True)
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         except:
#             raise exceptions.APIException(
#                 detail=serializer.errors, code=status.HTTP_400_BAD_REQUEST
#             )


# class Orders(APIView):
#     '''
    
#     '''
#     authentication_classes = [
#         CustomAuthentication,
#     ]
#     permission_classes = [
#         IsAuthenticated,
#     ]

#     def post(self, request, coupon_id):
#         user = User.objects.get(id=request.user.id)
#         coupon = Coupon.objects.get(coupon_id=coupon_id)
#         store = coupon.store_id
#         order_amount = request.data.get("order_amount")

#         if not user:
#             raise exceptions.APIException(detail="Error retrieving user data")

#         if not coupon:
#             raise exceptions.APIException(detail="Coupon not found")

#         if user.wallet >= coupon.coupon_price:
#             total = coupon.coupon_price * order_amount
#             user.wallet -= total
#             user.save()
#         else:
#             raise exceptions.APIException(detail="Insufficient funds", code=status.HTTP_400_BAD_REQUEST)

#         if not order_amount:
#             order_amount = 1

#         order = Order.objects.create(
#             user_id=user, store_id=store, coupon_id=coupon, order_amount=order_amount
#         )

#         OrderSerializer(instance=order)
#         return Response(data='Order placed', status=status.HTTP_200_OK)


# class UserOrders(APIView):
#     '''
    
#     '''
#     authentication_classes = [
#         CustomAuthentication,
#     ]
#     permission_classes = [
#         IsAuthenticated,
#     ]

#     def get(self, request):
#         orders = Order.objects.filter(user_id=request.user.id)

#         if not orders:
#             return Response(data="No orders found")

#         serializer = OrderSerializer(orders, many=True)

#         return Response(data=serializer.data, status=status.HTTP_200_OK)

