from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class EmailBackend(object):
    def authenticate(self, request, email=None, password=None):
        # User = get_user_model()
        try:
            user = User.objects.get(email=email)
            print(user.check_password(password))
            is_active = user.is_active
            if user.check_password(password) and is_active:
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None