from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CallbackView(APIView):

    def get(self, request):
        print(request.data.get('access_token'))
        access = request.data.get('access_token')
        return Response({
                            "success": "Callback Success",
                            "access_token":access
                        }, 
                        status=200
                        )
                        