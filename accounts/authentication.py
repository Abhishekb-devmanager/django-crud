from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import check_password
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from .models import User, UserPhone

class CustomAuthentication(authentication.BaseAuthentication):
    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password')
        phone_no = request.data.get('phone_no', None)
        if not email and not password:
            return None
        if not phone_no and not password:
            return None
        try:
            if email and password:
                user = User.objects.get(email=email)
            elif phone_no and password:
                phnobj = UserPhone.objects.get(phone_no=phone_no)
                user = User.objects.get(id=phnobj.owner_id)
                
            is_pwd_valid = check_password(password, user.password)
            if not is_pwd_valid:
                raise exceptions.AuthenticationFailed(_('Invalid credentials.'))
            if not user.is_active:
                raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        return user
        #return (user, user.auth_token)
                    

