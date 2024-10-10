from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth.models import User
User = get_user_model()

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = User
        try:
            user = user_model.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        user_model = User
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
