from django.urls import path
from .views import StoresList, StoreCoupons, Orders, UserOrders, AddStore, AddCoupons


urlpatterns = [
    path("stores/", StoresList.as_view(), name="stores list"),
    path('add_store/', AddStore.as_view(), name='add store'),
    path("coupons/<int:store_id>/", StoreCoupons.as_view(), name="coupons"),
    path('add_coupon/<int:store_id>/', AddCoupons.as_view(), name='add coupon'),
    path("order/<int:coupon_id>/", Orders.as_view(), name="order"),
    path("user_orders/", UserOrders.as_view(), name="user orders"),   
]
