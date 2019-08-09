from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import check_password
from django.conf import settings
from rest_framework import authentication
from rest_framework.authentication import get_authorization_header
from rest_framework import exceptions
from .models import User, UserPhone
from api.utility.helpertoken import token_expire_handler, is_token_expired, expires_in

class CustomAuthentication(authentication.BaseAuthentication):
    keyword = 'Bearer'
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token

    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, request):
        if not request.data:
            tuple_obj = self.authenticate_and_regenerate_token(request)
            return tuple_obj[0]
        email = request.data.get('email', None)
        password = request.data.get('password')
        phone_no = request.data.get('phone_no', None)

        if not email and not password:
            return None
        if not phone_no and not password:
            return None
        #TODO: Write Token refresh strategy or figure out how to call BearerTokenAuthentication
        try:
            if email and password:
                user = User.objects.get(email=email)
            if phone_no and password:
                phnobj = UserPhone.objects.get(phone_no=phone_no)
                user = User.objects.get(id=phnobj.owner_id)
                
            is_pwd_valid = check_password(password, user.password)
            if not is_pwd_valid:
                raise exceptions.AuthenticationFailed(_('Invalid credentials.'))
            if not user.is_active:
                raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
            
            #new token created in in case it has expired. 
            is_expired = token_expire_handler(user.auth_token)
            # if is_expired:  
            #     raise exceptions.AuthenticationFailed(_('The Token is expired'))

        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        return user

    def authenticate_and_regenerate_token(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        #This is required for the time comparison

        token = token_expire_handler(token)
        return (token.user, token)
                        
class BearerTokenAuthentication(authentication.TokenAuthentication):
    keyword = 'Bearer'
    
    # def authenticate_credentials(self, key):
    #     try:
    #         model = self.get_model()
    #         token = model.objects.get(key=key)
    #     except model.DoesNotExist:
    #         raise exceptions.AuthenticationFailed('Invalid token')

    #     if not token.user.is_active:
    #         raise exceptions.AuthenticationFailed('User inactive or deleted')

    #     # This is required for the time comparison
    #     token = token_expire_handler(token)

    #     return (token.user, token)