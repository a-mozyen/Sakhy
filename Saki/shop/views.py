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

class AddStore(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        store = AddStoreSerializer(data=request.data)

        if store.is_valid(raise_exception=True):
            store.save()
            return Response(data='Store added')
        else:
            raise exceptions.APIException(detail=store.errors)


class AddCoupons(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated,]
    def post(self, request, store_id):
        coupon_price = request.data.get('coupon_price')
        store = Store.objects.get(store_id=store_id)

        if not coupon_price:
            raise exceptions.APIException(detail='Field missing')
        
        coupon = Coupon.objects.create(
            store_id=store,
            coupon_price=coupon_price
        )
        serializer = AddCouponSerializer(instance=coupon)
        return Response(serializer.data)

class StoresList(APIView):
    def get(self, request):
        try:
            stores = Store.objects.all()
            serializer = StoreSerializer(instance=stores, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            raise exceptions.APIException(
                detail=serializer.errors, code=status.HTTP_400_BAD_REQUEST
            )


class StoreCoupons(APIView):
    def get(self, request, store_id):
        try:
            coupons = Coupon.objects.filter(store_id=store_id)
            serializer = CouponSerializer(instance=coupons, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            raise exceptions.APIException(
                detail=serializer.errors, code=status.HTTP_400_BAD_REQUEST
            )


class Orders(APIView):
    authentication_classes = [
        CustomAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, coupon_id):
        user = User.objects.get(id=request.user.id)
        coupon = Coupon.objects.get(coupon_id=coupon_id)
        store = coupon.store_id
        order_amount = request.data.get("order_amount")

        if not user:
            raise exceptions.APIException(detail="Error retrieving user data")

        if not coupon:
            raise exceptions.APIException(detail="Coupon not found")

        if user.wallet >= coupon.coupon_price:
            total = coupon.coupon_price * order_amount
            user.wallet -= total
            user.save()
        else:
            raise exceptions.APIException(detail="Insufficient funds", code=status.HTTP_400_BAD_REQUEST)

        if not order_amount:
            order_amount = 1

        order = Order.objects.create(
            user_id=user, store_id=store, coupon_id=coupon, order_amount=order_amount
        )

        OrderSerializer(instance=order)
        return Response(data='Order placed', status=status.HTTP_200_OK)


class UserOrders(APIView):
    authentication_classes = [
        CustomAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        orders = Order.objects.filter(user_id=request.user.id)

        if not orders:
            return exceptions.APIException(detail="No orders found")

        serializer = OrderSerializer(orders, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
