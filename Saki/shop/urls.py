from django.urls import path
# from .views import (
#     GetToken, RefreshToken, ListAllItems, CheckAvailablity, 
#     CheckBalance, Purchase, PurchaseDetails, AllPurchases)
from .views import StoresList, StoreCoupons, Orders, UserOrders, AddStore, AddCoupons

urlpatterns = [
    path("stores/", StoresList.as_view(), name="stores list"),
    path('add_store/', AddStore.as_view(), name='add store'),
    path("coupons/<int:store_id>/", StoreCoupons.as_view(), name="coupons"),
    path('add_coupon/<int:store_id>/', AddCoupons.as_view(), name='add coupon'),
    path("order/<int:coupon_id>/", Orders.as_view(), name="order"),
    path("user_orders/", UserOrders.as_view(), name="user orders"),
    # path("get_token/", GetToken.as_view(), name='get token'),
    # path("refresh_token/", RefreshToken.as_view(), name='refresh token'),
    # path("items/", ListAllItems.as_view(), name='list items'),
    # path('check_items/', CheckAvailablity.as_view(), name='check items'),
    # path('check_balance/', CheckBalance.as_view(), name='check balance'),
    # path('purchase/', Purchase.as_view(), name='purchase'),
    # path('purchase_details/', PurchaseDetails.as_view(), name='purchase details'),
    # path('purchase_history/', AllPurchases.as_view(), name='purchase history')
]
