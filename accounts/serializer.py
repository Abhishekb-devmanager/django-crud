from rest_framework import serializers
from .models import User, UserPhone
from api.utility.flatten import FlattenMixin
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from api.utility.customexceptions import ServiceUnavailable, BadRequest, ValidationError

class UserPhoneSerializer(serializers.ModelSerializer):
     """Serializer to map the UserPhone Model instance into JSON format.Nested under UserSerializer"""
     class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = UserPhone
        fields = (
            'phone_no',
        )
        
        def __str__(self):
            return self.phone_no

        
class UserSerializer(FlattenMixin, serializers.ModelSerializer):
    """Serializer to map the User Model instance into JSON format."""

    #Changing the name of var to user_phone
    #
    user_phone = UserPhoneSerializer(many=False)
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = (
            'email',
            'password',
            'date_joined', 
            'active',
            'admin',
            'reader',
            'staff',
            'user_phone'
        )
        flatten = [('user_phone', UserPhoneSerializer)]
    
    def create(self, validated_data):

        if 'user_phone' in validated_data:
            incoming_phn_no = validated_data.pop('user_phone')
            usrObj = User.objects.create(**validated_data)
            UserPhone.objects.create(owner=usrObj, phone_no=incoming_phn_no.get('phone_no'))
        else:
           usrObj = User.objects.create(**validated_data) 
        return usrObj

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)       
        instance.save()
        return instance



class UserSerializerWithoutPhone(serializers.ModelSerializer):
    """Serializer to map the User Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = User
        # This allow us to hide password from the serializer representation but accept it.
        # Pwd cannot be exposed in responses.
        extra_kwargs = {'password': {'write_only': True}}
        fields = (
            'email',
            'password',
            'date_joined', 
            'active',
            'admin',
            'reader',
            'staff',
        )

    def create(self, validated_data):
        usrObj = User.objects.create(**validated_data) 
        return usrObj
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        # should not update anyother parameter using apis. Pwd updation yet to come.
        #TODO: Password should not be updated like this it should have a changepassword 
        instance.save()
        return instance

    def validate(self, data):
        # here data has all the fields which have validated values
         # so we can create a User instance out of it
         user = User(**data)
         # get the password from the data
         password = data.get('password')
         errors = dict() 
         try:
             # validate the password and catch the exception
             validators.validate_password(password=password, user=user)
         # the exception raised here is different than serializers.ValidationError
         except exceptions.ValidationError as e:
             errors['password'] = list(e.messages)
         if errors:
             raise serializers.ValidationError(errors)
         return super(UserSerializerWithoutPhone, self).validate(data)