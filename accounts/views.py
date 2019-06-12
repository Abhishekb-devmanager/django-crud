from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import Http404, QueryDict
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.views import APIView
from rest_framework.response import Response
from api.utility.customexceptions import ServiceUnavailable, BadRequest
from rest_framework import status
from .serializer import UserSerializer, UserPhoneSerializer, UserSerializerWithoutPhone
from .models import User, UserManager
import copy

class UserView(APIView):
    """This class defines the create behavior of our rest api."""
    
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk = None):
        if pk:
            users = self.get_object(pk=pk)
            is_many=False
        else:
            users = User.objects.all()
            is_many = True

        serializer = UserSerializer(users, many=is_many)
        return Response(({"users":serializer.data}))
        
    #how to disallow request - plan/24 with post action
    #TODO: Need to check the incoming request data structure, avoid any key errors

    def post(self, request):
        """Handle update requests user/<id>.
        Returns 201 Resource created with created objects as a list."""

        changed_request_data = self.prepare_data(request.data)
        #if changed_request_data.data.get('error') is None:
        if changed_request_data.get('user_phone') is None:
            serializer = UserSerializerWithoutPhone(data=changed_request_data, many=False)
        else:
            serializer = UserSerializer(data=changed_request_data, many=False)
        
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()

        return Response({
                            "success": "User {} created successfully".format(user_saved.email),
                            "users":serializer.data
                        }, 
                        status=201
                        )
        #else:
        #   raise ValueError({"error":changed_request_data.data.get('error')})
            
    def put(self,request,pk):
        """Handle update requests plan/<id>.
        Returns 200 with updated object.
        This does not creates object if it does not exists."""

        saved_user = self.get_object(pk=pk)

        #Supports partial request - PATCH in Django might be broken.
        serializer = UserSerializer(instance=saved_user, data=request.data, partial=True)

        #TODO: this did not raise exception when request.data was mistakenly supplied
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()

        return Response({
                "success": "User '{}' updated successfully".format(user_saved.email),
                "users":serializer.data
            }, 
            status=200)

    def delete(self, request, pk):
        # Get object with this pk
        user = self.get_object(pk=pk)
        user.delete()
        return Response({"message": "User with id `{}` has been deleted.".format(pk)},status=204)

    #https://stackoverflow.com/questions/1451138/how-can-i-get-the-domain-name-of-my-site-within-a-django-template
    
    def autogenerate_email(self, req, phn):
        current_site = get_current_site(req).domain
        incoming_phn_str = req.data.get('user_phone')
        autogenerated_email = "{}@{}".format(incoming_phn_str,current_site)        
        return autogenerated_email

    #https://stackoverflow.com/questions/2465921/how-to-copy-a-dictionary-and-only-edit-the-copy/2465951#2465951

    def prepare_request_data_with_missing_email(self, req):
        current_site = get_current_site(req).domain
        if req.get('phone_no') is not None:
            incoming_phn_str = req.get('phone_no')

        autogenerated_email = "{}@{}".format(incoming_phn_str,current_site)   
        req['email'] = autogenerated_email
        return req
    
    # This converts the str user_phone to a valid dict 
    def prepare_request_data_for_phone(self, req):
        if req.get('phone_no') is not None:
            phn_recvd = req.get('phone_no')
        
        user_phone_dict = dict()
        user_phone_dict['phone_no'] = phn_recvd
        req.pop('phone_no')
        req['user_phone'] = user_phone_dict
        return req

    def prepare_data(self, req):
        try:
            is_many = isinstance(req, list)
            if is_many:
                raise TypeError('Multi user entry is prohibited')

            if req.get('email') is None and req.get('phone_no') is None:
                raise KeyError('An email or a phone number is required to onboard.')
            if req.get('password') is None:
                raise KeyError('A password is mandatory to be assigned')
            
            #create a copy of the request data instead of editing the original data received.
            if req.get('phone_no') is None and req.get('email') is not None:
                prepared_data = req
            else:
                prepared_data = copy.deepcopy(req)

            if req.get('email') is None:
                prepared_data = self.prepare_request_data_with_missing_email(prepared_data)

            if req.get('phone_no') is not None:
                prepared_data = self.prepare_request_data_for_phone(prepared_data)

            return prepared_data

        except (KeyError, TypeError) as err:
            raise BadRequest(detail=err) 

    def get_phone_from_request_data(self, req):
        if req.data.get('user_phone') is not None:
            phn_recvd = req.data.get('user_phone').get('phone_no')
        return phn_recvd

    def remove_phone_from_request_data(self, req):
        copy_req = copy.deepcopy(req.data)
        if copy_req.get('user_phone') is not None:
            copy_req.pop('user_phone')
        return copy_req