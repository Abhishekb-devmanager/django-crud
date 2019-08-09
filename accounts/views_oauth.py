from django.contrib.sites.shortcuts import get_current_site
from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import JsonResponse
import json, re

# Creating this view to test OAuth protected end point.
# ProtectedResourceView - is a subclass View and not APIView 
# Thus it does not provides automatic rendering of JSON or HTML, 
# You will need to declare the JsonReponse renderer. 
# Renderer provides a handshake between request,
# response content type in needed format like json or html. 
# client specifies the request media type what kind of response is needed.
# Accept header also does the same 
# Check the /o urls defined in urls.py for end point.
class AuthorizeView(ProtectedResourceView):
    """This is called when the authorize token is received in a redirection URL specified"""  
    
    def get(self,request):
        regex = re.compile('^HTTP_')
        header_tuples = []
        for (header, value) in request.META.items():
            if header.startswith('HTTP_'):
                key = regex.sub('', header)
                header_tuples.append((key, value))
                headers_dict= dict(header_tuples)

        return JsonResponse({
            "success": "You have granted SampleApp access to your IE details",
            "all_headers": headers_dict
            }, 
            status=200
            )

