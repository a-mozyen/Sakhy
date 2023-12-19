from django.urls import path
from .views import Register, Login, UserProfile, Logout, Verify_Otp

urlpatterns = [
    # path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("verify/", Verify_Otp.as_view(), name='login verify'),
    path("user_profile/", UserProfile.as_view(), name="user profile"),
    path("logout/", Logout.as_view(), name="logout"),
]
