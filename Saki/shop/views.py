from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
# from .serializers import (StoreSerializer, CouponSerializer, OrderSerializer, 
#                           AddStoreSerializer, AddCouponSerializer)
from user.serializers import UserSerializer
# from .models import Store, Coupon, Order
from user.models import User
from user.authentications import CustomAuthentication
from rest_framework.permissions import IsAuthenticated
import requests
import json
from .daleel_tokens import create_token, daleel_token


class GetToken(APIView):
    def post(self, request):
        url = "https://daleelapi.com/api/v1/oauth/token"

        payload = {
            'grant_type': 'password',
            'client_id': '2',
            'client_secret': 'D1uvg3aUd79fDIvqduYlaV3q1b59XztrPPooADyDrIo=',
            'username': 'merchants.api@daleelstore.com',
            'password': 'ABC12345'
            }
        
        header = {
        'Content-Type': 'application/x-www-form-urlencoded'
        # 'Content-Type': 'application/json' #x-www-form-urlencoded
        }

        get_token = requests.post(url=url, headers=header, data=payload)
        token = get_token.json()

        daleel_auth_token = create_token(
            token_type=token['token_type'], 
            access_token=token['access_token'],
            refresh_token=token['refresh_token']
            )
        response = Response(data='Successfull', status=status.HTTP_201_CREATED)
        response.set_cookie(key='daleeljwt', value=daleel_auth_token, httponly=True)
        
        return response
        # return Response(data=token)
    
    # curl -X POST "https://daleelapi.com/api/v1/oauth/token" -H "Content-Type: application/json" -d '{"grant_type": "password", "client_id": "2", "client_secret": "D1uvg3aUd79fDIvqduYlaV3q1b59XztrPPooADyDrIo=", "username": "merchants.api@daleelstore.com", "password": "ABC12345"}'
    

class RefreshToken(APIView):
    def post(self, request):
        token = daleel_token(request=request)
        refresh_token = token['refresh_token']

        url = "https://daleelapi.com/api/v1/oauth/token"
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": "2",
            "client_secret": "D1uvg3aUd79fDIvqduYlaV3q1b59XztrPPooADyDrIo="
        }
        
        response = requests.post(url=url, headers=headers, data=payload)
        re_token = response.json()

        new_token = create_token(
            token_type=re_token['token_type'], 
            access_token=re_token['access_token'],
            refresh_token=re_token['refresh_token']
        )

        response = Response(status=status.HTTP_201_CREATED)
        response.set_cookie(key='daleeljwt', value=new_token, httponly=True)
        
        return response


class ListAllItems(APIView):
    def post(self, request):
        token = daleel_token(request=request)
        access_token = token['access_token']
        token_type = token['token_type']


        url = "https://daleelapi.com/api/v1/get_items"

        headers = {
        'Content-Type': 'application/json',#x-www-form-urlencoded
        'Authorization': f'{token_type} {access_token}',
        'lang': 'ar'
        }

        payload = {}
        
        response = requests.request("POST", url, headers=headers, data=payload)
        items = response.json()

        return Response(data=items)
    

class CheckAvailablity(APIView):
    def post(self, request):
        token = daleel_token(request=request)
        access_token = token['access_token']
        token_type = token['token_type']

        url = "https://daleelapi.com/api/v1/check_item"

        headers = {
            # 'Content-Type': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'{token_type} {access_token}'
            }
        
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')
        
        payload = {
            "item_id": item_id,
            "qty": quantity
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        check = response.json()
        
        return Response(data=check)
    

class CheckBalance(APIView):
    def post(self, request):
        token = daleel_token(request=request)
        access_token = token['access_token']
        token_type = token['token_type']

        url = "https://daleelapi.com/api/v1/get_balance"

        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'{token_type} {access_token}'
        }

        payload = {}

        response = requests.request("POST", url, headers=headers, data=payload)
        balance = response.json()

        return Response(data=balance)
    

class Purchase(APIView):
    def post(self, request):
        token = daleel_token(request=request)
        access_token = token['access_token']
        token_type = token['token_type']

        url = "https://daleelapi.com/api/v1/purchase"

        headers = {
        # 'Content-Type': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'{token_type} {access_token}'
        }

        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')

        payload = {
            "item_id": "31",#item_id,
            "qty": "1"#quantity
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        purchase = response.json()

        return Response(data=purchase)


class PurchaseDetails(APIView):
    def post(self, request):
        token = daleel_token(request=request)
        access_token = token['access_token']
        token_type = token['token_type']

        url = "https://daleelapi.com/api/v1/purchase_details"

        headers = {
        # 'Content-Type': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'{token_type} {access_token}'
        }

        Purchase_id = request.data.get('Purchase_id')
        payload = {
            "purchase_id": Purchase_id
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        details = response.json()

        return Response(data=details)


class AllPurchases(APIView):
    def post(self, request):
        token = daleel_token(request=request)
        access_token = token['access_token']
        token_type = token['token_type']

        url = "https://daleelapi.com/api/v1/all_purchase"

        payload = {}

        headers = {
        'Authorization': f'{token_type} {access_token}'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        purcheses = response.json()

        return Response(data=purcheses)
    

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

