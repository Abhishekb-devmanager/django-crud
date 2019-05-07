from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from .models import Plan
import json

# Create your tests here.
class PlanModelTestCase(TestCase):
    """This class defines the test suite for the Plans model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.plan = Plan(
                        plan_name='Monthly', 
                        description='This is test description',
                        amount=99,
                        currency='INR',
                        period= 'monthly',
                        interval= 1,
                        notes='Test Notes'
                    )

    def test_model_can_create_a_plan(self):
        """Test the plan model can create a plan."""
        old_count = Plan.objects.count()
        self.plan.save()
        new_count = Plan.objects.count()
        self.assertNotEqual(old_count, new_count)

class PlanViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
         #fresh plan object created.
        self.plan_data = {
                        'plan_name': 'Monthly Plan', 
                        'description': 'This is test description', 
                        'amount': '99', 
                        'currency': 'INR',
                        'period': 'monthly',
                        'interval': 1,
                        'notes': 'Test Notes'
                         }
        #testing update to the fresh plan created.
        self.valid_plan_data_payload = {
                        'plan_name': 'Fortnightly Plan', 
                        'description': 'This is test description', 
                        'amount': '99', 
                        'currency': 'INR',
                        'period': 'monthly',
                        'interval': 1,
                        'notes': 'Test Notes'
                         }
        #currency is missing
        self.invalid_plan_data_payload_1 = {
                        'plan_name': 'Fortnightly Plan', 
                        'description': 'This is test description', 
                        'amount': '', 
                        'currency': 'INR',
                        'period': 'monthly',
                        'interval': 1,
                        'notes': 'Test Notes'
                         }
        #currency is non-integer
        self.invalid_plan_data_payload_2 = {
                        'plan_name': 'Fortnightly Plan', 
                        'description': 'This is test description', 
                        'amount': 'NinetyNine', 
                        'currency': 'INR',
                        'period': 'monthly',
                        'interval': 1,
                        'notes': 'Test Notes'
                         }
        #period is missing
        self.invalid_plan_data_payload_3 = {
                        'plan_name': 'Fortnightly Plan', 
                        'description': 'This is test description', 
                        'amount': 'NinetyNine', 
                        'currency': 'INR',
                        'period': '',
                        'interval': 1,
                        'notes': 'Test Notes'
                         }

    def createPlan(self):
        self.response = self.client.post(
            reverse('create'),
            self.plan_data,
            format='json'
        )
    
    def createPlanDictionary(self):
        """This will create plan and return the response as a dictionary."""
        self.createPlan()
        self.response = self.client.get(
            reverse('create'),
            format='json'
        )
        # for now let #print a success message
        response_dict = json.loads(self.response.content)
        #print(response_dict)
        dictcount = len(response_dict)
        ##print(type(response_dict))
        #mesg = "Fetched %d Plans successfully" % (dictcount)
        #print(mesg)
        # #TODO: this may fail if there will be 2 plans in the response.
        # # Need to add iteration 
        # response_dict = json.loads(self.response.content)
        #print(response_dict[0])
        return response_dict[0]
        
    # def deletePlan(self, planId):
    #     self.plan_data = {
    #                     'plan_name': 'Fortnightly Plan', 
    #                     'description': 'This is test description', 
    #                     'amount': '99', 
    #                     'currency': 'INR',
    #                     'period': 'monthly',
    #                     'interval': 1,
    #                     'notes': 'Test Notes'
    #                      }
    #     self.response = self.client.delete(
    #         reverse('details'),
    #         self.plan_data,
    #         format='json'
    #     )


    def test_api_can_create_a_plan(self):
        """Test the api has plan creation capability."""
        #Create a plan using API, also it can be created using plan model.
        self.createPlan()
        #print(self.response.json())
        #print(self.response.json()['description'])
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED, msg="Plan created successfully")
        self.assertContains(self.response, 'Monthly Plan', count=1, status_code=201)

    def test_api_can_get_plan(self):
        """Test the api fetch plans."""
        #Again creating plan to make this test independent, it seems
        #Test DB is destroyed before this test can fetch the created object.
        response_dict = self.createPlanDictionary()
        self.assertEqual(self.response.status_code, status.HTTP_200_OK, msg="Fetching Plans Failed")
        self.assertIs((len(response_dict)>0),True, msg="Fetching Plans Failed")

    #HTTP status code 200 OK for a successful PUT of an update to an existing resource.
    # No response body needed. (Per Section 9.6, 204 No Content is even more appropriate.)
    # and any other relevant URIs and metadata of the resource echoed in the response body. 
    # (RFC 2616 Section 10.2.2)

    def test_api_can_update_if_plan_already_exists(self):
        """Test the api update preexisting plans."""
        response_dict = self.createPlanDictionary()
        #mesg = "Updating name from %s to %s" % (response_dict['plan_name'],self.valid_plan_data_payload['plan_name'])
        #print(mesg)

        self.response = self.client.put(
            reverse('details', kwargs={'pk':response_dict['id']}),
            data=self.valid_plan_data_payload,
            format='json'
        )
        #get updated plan
        get_response = self.client.get(
            reverse('details', kwargs={'pk':response_dict['id']}),
            format='json'
        )
        #check if plan name updated
        self.assertContains(get_response, 'Fortnightly Plan')
        #check status code
        self.assertEqual(
            self.response.status_code, 
            status.HTTP_204_NO_CONTENT, 
            msg="Incorrect status code. Expected 204"
        )
        
        
    #HTTP status code 201 Created for a successful PUT of a new resource, 
    #with the most specific URI for the new resource returned in the Location
    #header field 

    def test_api_can_create_if_plan_not_exists(self):
        """Test the api create if plan does not exists."""

            #There cannot be a 10th plan, 
            #resource does not exist
        self.response = self.client.put(
            reverse('details', kwargs={'pk':10}), 
            data=self.valid_plan_data_payload,
            format='json'
        )
        self.assertEqual(
            self.response.status_code, 
            status.HTTP_201_CREATED, 
            msg="Incorrect response code. Expected 201"
        )
        self.assertIs(
            self.response.has_header('Location'), 
            True, 
            msg="Location header should be present with URI of resource created"
        )
        locationHeaderURL = r'^planlist/(?P<pk>[0-9]+)/$'
        self.assertRegex(
            self.response.get('Location'),
            locationHeaderURL,
            msg="Not a valid resource URL"
        )


    def test_api_rejects_update_with_invalid_data(self):
        """Test the api rejects invalid put request."""
        response_dict = self.createPlanDictionary()
        mesg = "Updating name from %s to %s" % (response_dict['plan_name'],self.invalid_plan_data_payload_1['plan_name'])
        ##print(mesg)
        self.response = self.client.put(
            reverse('details', kwargs={'pk':response_dict['id']}),
            data=self.invalid_plan_data_payload_1,
            format='json'
        )
        self.assertEqual(
            self.response.status_code, 
            status.HTTP_400_BAD_REQUEST, 
            msg="Incorrect response code. Expected 400."
        )

        self.response = self.client.put(
            reverse('details', kwargs={'pk':response_dict['id']}),
            data=self.invalid_plan_data_payload_2,
            format='json'
        )
        self.assertEqual(
            self.response.status_code, 
            status.HTTP_400_BAD_REQUEST, 
            msg="Incorrect response code. Expected 400."
        )

        self.response = self.client.put(
            reverse('details', kwargs={'pk':response_dict['id']}),
            data=self.invalid_plan_data_payload_3,
            format='json'
        )
        self.assertEqual(
            self.response.status_code, 
            status.HTTP_400_BAD_REQUEST, 
            msg="Incorrect response code. Expected 400."
        )
    #HTTP status code 409 Conflict for a PUT that is unsuccessful 
    #due to a 3rd-party modification, with a list of differences 
    #between the attempted update and the current resource in the response body. 
    # RFC 2616 Section 10.4.10)

    #HTTP status code 400 Bad Request for an unsuccessful PUT, 
    # with natural-language text (such as English) in the response body 
    # that explains why the PUT failed. (RFC 2616 Section 10.4)