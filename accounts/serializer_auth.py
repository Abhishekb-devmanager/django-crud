from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework import exceptions
from api.utility.helpertoken import token_expire_handler, expires_in, get_user_from_context, is_request_authenticated
from .models import User, UserPhone
from collections import OrderedDict

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=True)
    password = serializers.CharField(min_length=None, 
                                     allow_blank=False, 
                                     trim_whitespace=True
                                    )
    token = serializers.CharField(allow_blank=True, required=False)
    expires_in = serializers.DurationField(required=False)
    
    def validate(self, data):
        if is_request_authenticated(self):
            data['authenticated_user'] = get_user_from_context(self)
            data['token'] = data['authenticated_user'].auth_token
            data['expires_in']= expires_in(data['token'])
            return data

        email = data.get('email', None)
        password = data.get('password')

        if email and password:
            authenticated_user  = authenticate(request=self.context.get('request'))
            if not authenticated_user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['authenticated_user']= authenticated_user
        data['token']= authenticated_user.auth_token
        data['expires_in']= expires_in(authenticated_user.auth_token)
        return data

class AuthTokenSerializerWithPhone(serializers.Serializer):
    phone_no = serializers.CharField(allow_blank=True)
    password = serializers.CharField(min_length=None, 
                                    allow_blank=False, 
                                    trim_whitespace=True
                                    )
    token = serializers.CharField(allow_blank=True, required=False)
    expires_in = serializers.DurationField(required=False)

    def validate(self, data):
        if is_request_authenticated(self): 
            data['authenticated_user'] = get_user_from_context(self)
            data['token'] = data['authenticated_user'].auth_token
            data['expires_in']= expires_in(data['token'])
            return data

        phone_no = data.get('phone_no', None)
        password = data.get('password')
        

        if phone_no and password:
            authenticated_user  = authenticate(request=self.context.get('request'))
            if not authenticated_user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "phone no" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['authenticated_user'] = authenticated_user
        data['token'] = authenticated_user.auth_token
        data['expires_in']= expires_in(authenticated_user.auth_token)

        return data


class RefreshTokenSerializer(serializers.Serializer):
    token = serializers.CharField(allow_blank=True, required=False)
    expires_in = serializers.DurationField(required=False)

    def validate(self, data):        
        if is_request_authenticated(self):
            data['authenticated_user'] = get_user_from_context(self)
            data['token'] = data['authenticated_user'].auth_token
            data['expires_in']= expires_in(data['token'])
            return data

        authenticated_user  = authenticate(request=self.context.get('request'))
        if not authenticated_user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        

        data['authenticated_user'] = authenticated_user
        data['token'] = authenticated_user.auth_token
        data['expires_in']= expires_in(authenticated_user.auth_token)

        return data