from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .serializer_auth import CustomAuthTokenSerializer, AuthTokenSerializerWithPhone, RefreshTokenSerializer
   
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_auth_serializer(prepared_data=request.data)
        serializer = serializer(data=request.data,context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['authenticated_user'] 

        return Response({
            "success": "User {} authenticated successfully".format(user.email),
            "auth":serializer.data,
        }, 
        status=201)
    
    def get_auth_serializer(self,prepared_data):
        #default serializer to be returned.
        serializer_class = RefreshTokenSerializer

        try:
            if prepared_data is None:
                raise TypeError('Serializer needs data to initialize. Prepared data is None')
        except TypeError as err:
            return err

        email = prepared_data.get('email', None)
        if email:
            serializer_class = CustomAuthTokenSerializer

        phone_no = prepared_data.get('phone_no', None)
        if phone_no:
            serializer_class = AuthTokenSerializerWithPhone

        return serializer_class