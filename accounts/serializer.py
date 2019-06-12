from rest_framework import serializers
from .models import User, UserPhone
from api.utility.flatten import FlattenMixin
class UserPhoneSerializer(serializers.ModelSerializer):
     """Serializer to map the UserPhone Model instance into JSON format."""
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
        fields = (
            'email',
            'date_joined', 
            'active',
            'admin',
            'reader',
            'staff',
            'user_phone'
        )
        flatten = [('user_phone', UserPhoneSerializer)]
    
    def create(self, validated_data):
        #refer to writable nested 

        if 'user_phone' in validated_data:
            incoming_phn_no = validated_data.pop('user_phone')
            usrObj = User.objects.create(**validated_data)
            UserPhone.objects.create(owner=usrObj, phone_no=incoming_phn_no.get('phone_no'))
        else:
           usrObj = User.objects.create(**validated_data) 
       
        return usrObj

    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.phone_no = validated_data.get('phone_no', instance.phone_no)
    #     # should not update anyother parameter using apis. Pwd updation yet to come.
    #     instance.save()
    #     return instance


class UserSerializerWithoutPhone(serializers.ModelSerializer):
    """Serializer to map the User Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = User
        fields = (
            'email',
            'date_joined', 
            'active',
            'admin',
            'reader',
            'staff',
        )

    def create(self, validated_data):
        #refer to writable nested 
        usrObj = User.objects.create(**validated_data) 
        return usrObj