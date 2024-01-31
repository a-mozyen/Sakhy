from datetime import datetime, timedelta
from django.utils import timezone


access_token_expiry = datetime.utcnow() + timedelta(minutes=5)
refresh_token_expiry = datetime.utcnow() + timedelta(minutes=10)


otp_expiry = timezone.now()+timezone.timedelta(minutes=5)