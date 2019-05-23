from django.shortcuts import render
from django.http import Http404, QueryDict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import PlanSerializer, PlanFeatureSerializer
from .models import Plan, PlanFeature

class PlanView(APIView):
    """This class defines the create behavior of our rest api."""

    def get_object(self, pk):
        try:
            return Plan.objects.get(pk=pk)
        except Plan.DoesNotExist:
            raise Http404

    def get(self, request, pk = None):
        if pk:
            plans = self.get_object(pk=pk)
            is_many=False
        else:
            plans = Plan.objects.all()
            is_many = True

        serializer = PlanSerializer(plans, many=is_many)
        return Response(({"plans":serializer.data}))
        
    #how to disallow request - plan/24 with post action
    #TODO: Need to check the incoming request data structure, avoid any key errors
    #TODO: Need to validate the data through middleware
    def post(self, request):
        """Handle update requests plan/<id>.Returns 201 Resource created with created objects as a list."""
        #Create a plan from the above data, 
        #mulitple plan object can also be created if a list of plans is supplied
        # is_many set to false if it is a dict.
        # remove plans key - request does not need to have a key at the root, we assume its plan data.
        is_many = isinstance(request.data, list)

        #many = true needed to support saving of a list of plan objs
        serializer = PlanSerializer(data=request.data, many=is_many)

        if serializer.is_valid(raise_exception=True):
            plan_saved = serializer.save()
            
        # ternary operator - right side of if expression else is executed
        pn =  plan_saved[0].plan_name if is_many else plan_saved.plan_name
        return Response({
                            "success": "Plan {} created successfully".format(pn),
                            "plans":serializer.data
                        }, 
                        status=201)

    def put(self,request,pk):
        """Handle update requests plan/<id>.
        Returns 200 with updated object.
        This does not creates object if it does not exists."""

        saved_plan = self.get_object(pk=pk)

        #Supports partial request - PATCH in Django might be broken.
        serializer = PlanSerializer(instance=saved_plan, data=request.data, partial=True)

        #TODO: this did not raise exception when request.data was mistakenly supplied
        if serializer.is_valid(raise_exception=True):
            plan_saved = serializer.save()

        return Response({
                "success": "Plan '{}' updated successfully".format(plan_saved.plan_name),
                "plans":serializer.data
            }, 
            status=200)

    def delete(self, request, pk):
        # Get object with this pk
        planObject = self.get_object(pk=pk)
        planObject.delete()
        return Response({"message": "Plan with id `{}` has been deleted.".format(pk)},status=204)

class PlanFeatureView(APIView):
        
    def get_object(self, pk):
            try:
                planObject = Plan.objects.get(pk=pk)
                return planObject.features
                
            except Plan.DoesNotExist:
                raise Http404

    def get(self, request, pk = None):
        if pk:
            feature_list = self.get_object(pk=pk)
            is_many=False
        else:
            feature_list = PlanFeature.objects.all()
            is_many = True

        serializer = PlanFeatureSerializer(feature_list, many=is_many)
        return Response(({"features":serializer.data}))
        
    def put(self,request,pk):
        """Handle update requests plan/<id>.
        Returns 200 with updated object.
        This does not creates object if it does not exists."""

        saved_plan = self.get_object(pk=pk)

        #Supports partial request - PATCH in Django might be broken.
        serializer = PlanFeatureSerializer(instance=saved_plan, data=request.data, partial=True)

        #TODO: this did not raise exception when request.data was mistakenly supplied
        if serializer.is_valid(raise_exception=True):
            plan_saved = serializer.save()

        return Response({
                "success": "Plan '{}' updated successfully".format(plan_saved.plan_name),
                "plans":serializer.data
            }, 
            status=200)

# class DetailsPlanView(generics.RetrieveUpdateDestroyAPIView):
#     """This class handles the http GET, PUT and DELETE requests."""
#     queryset = Plan.objects.all()
#     serializer_class = PlanSerializer

#     def get_queryset(self):
#         plan = self.kwargs['pk']
#         return Plan.objects.filter(id=plan)



#     def put(self,request,pk,format=None):
#         plan = self.get_queryset(pk)
#         serializer=PlanSerializer(plan,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    

    #update
    # def perform_update(self, serializer):
    #     """Save the edited plan."""
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


