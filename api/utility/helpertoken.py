from rest_framework.authtoken.models import Token

from datetime import timedelta
from django.utils import timezone
from django.conf import settings

#this return left time
def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return left_time

# token checker if token expired or not
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds = 0)

# if token is expired new token will be established
# If token is expired then it will be removed
# and new one with different key will be created
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user = token.user)
    return token
    #return is_expired, token
def is_request_authenticated(serializer_obj):
    is_req_authenticated = False
    request = serializer_obj.context.get("request")
    if request and hasattr(request, "user"):
        if request.user.is_authenticated:
            is_req_authenticated = True
    return is_req_authenticated

def get_user_from_context(serializer_obj):
    request = serializer_obj.context.get("request")
    if request and hasattr(request, "user"):
        return request.user