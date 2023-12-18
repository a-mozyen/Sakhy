from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import MinLengthValidator


class UserManager(BaseUserManager):
    def create_user(
        self,
        username,
        email,
        country_code,
        phone,
        wallet,
        income,
        income_source,
        marital_status,
        is_admin,
        is_active
    ):
        user = self.model()
        user.username = username
        user.email = email
        user.country_code = country_code
        user.phone = phone
        user.wallet = wallet
        user.income = income
        user.income_source = income_source
        user.marital_status = marital_status
        user.is_admin = is_admin
        user.is_active = is_active

        user.save()
        return user

    def create_superuser(self, email, phone, country_code, is_admin=True, is_active=True):
        user = self.model(
            email=email, phone=phone, country_code=country_code, is_admin=is_admin, is_active=is_active
        )

        user.save()
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True, null=True)
    country_code = models.CharField(max_length=5, default='+966')
    phone = models.CharField(max_length=9, validators=[MinLengthValidator(limit_value=9)], unique=True)
    wallet = models.FloatField(default=0)
    income = models.IntegerField(null=True)
    income_source = models.CharField(max_length=15, null=True)
    marital_status = models.CharField(max_length=15, null=True)
    password = None
    last_login = None
    is_admin = False
    is_active = True

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    # def save(self, *args, **kwargs):
    #     self.email = self.email.lower()
    #     super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

class Otp(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    utilized = models.BooleanField(default=False)
    expirey = models.DateTimeField()
