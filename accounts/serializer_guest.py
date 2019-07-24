from rest_framework import serializers
from .models import GuestEmail

class GuestEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestEmail
        fields = (
            'email',
            'phone_no',
            'code'
        )

        def __str__(self):
            return self.email
        
    def create(self, validated_data):
        new_email = validated_data['email']
        #delete if the incoming email is already saved. This is applicable only to guest user
        try:
            pre_existing_email = GuestEmail.objects.get(email=new_email)
        except GuestEmail.DoesNotExist:
            pre_existing_email = None

        if pre_existing_email is not None:
            pre_existing_email.delete()
        guestuser = GuestEmail.objects.create(**validated_data)
        return guestuser
