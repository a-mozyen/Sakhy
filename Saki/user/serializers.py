from rest_framework import serializers
from .models import User, Otp


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ("id", "wallet")

class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = "__all__"
        read_only_fields = "__all__"