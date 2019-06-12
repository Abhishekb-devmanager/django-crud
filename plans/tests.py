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
                        plan_name="Monthly", 
                        description="This is test description",
                        amount=99,
                        currency="INR",
                        period= "monthly",
                        interval= 1,
                        notes="Test Notes"
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
        self.plan_data = [{
                            "plan_name": "Monthly Plan 1999999", 
                            "description": "This is test description", 
                            "amount": 99, 
                            "currency": "INR",
                            "period": "monthly",
                            "interval": 1,
                            "notes": "Test Notes"
                        }]
                         
        #testing update to the fresh plan created.
        self.valid_plan_data_payload = {
                                        "plan_name": "Put Monthly Plan 1999999", 
                                        "description": "This is test description", 
                                        "amount": 99, 
                                        "currency": "INR",
                                        "period": "monthly",
                                        "interval": 1,
                                        "notes": "Test Notes",
                                            "features":[{
                                                "display_text":"TF1 Test"
                                            }]
                                        }
        #amount is missing
        self.invalid_plan_data_payload_1 = {
                        "plan_name": "Fortnightly Plan", 
                        "description": "This is test description", 
                        "amount": "", 
                        "currency": "INR",
                        "period": "monthly",
                        "interval": 1,
                        "notes": "Test Notes"
                         }
        #currency is non-integer
        self.invalid_plan_data_payload_2 = {
                        "plan_name": "Fortnightly Plan", 
                        "description": "This is test description", 
                        "amount": "NinetyNine", 
                        "currency": "INR",
                        "period": "monthly",
                        "interval": 1,
                        "notes": "Test Notes"
                         }
        #period is missing
        self.invalid_plan_data_payload_3 = {
                        "plan_name": "Fortnightly Plan", 
                        "description": "This is test description", 
                        "amount": "NinetyNine", 
                        "currency": "INR",
                        "period": "",
                        "interval": 1,
                        "notes": "Test Notes"
                         }

    def test_api_cannot_create_a_plan_without_features(self):
        """Test the api has plan creation capability."""
        #Create a plan using API, also it can be created using plan model.
        response = self.client.post(
            reverse("create"),
            self.plan_data,
            format="json"
        )    
        #print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg="Plan creation failed.")


    def test_api_can_create_a_plan_with_features(self):
        """Test the api has plan creation capability."""
        #Create a plan using API, also it can be created using plan model.
        response = self.client.post(
            reverse("create"),
                [{
                    "plan_name": "Monthly Plan 234", 
                    "description": "This is test description", 
                    "amount": 99, 
                    "currency": "INR",
                    "period": "monthly",
                    "interval": 1,
                    "notes": "Test Notes",
                    "features":[{
                    				"display_text":"TF1 Test"
                    			},
                    			{
                    				"display_text":"TF2 Test"
                    			},
                    			{
                    				"display_text":"TF3 Test"
                    			}]
                }],
                format="json"
        )    
        #print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Plan creation failed.")
        self.assertContains(response, "Monthly Plan 234", status_code=201)

    def test_api_cannot_create_a_plan_without_amount(self):
        """Test the api has plan creation capability."""
        #Create a plan using API, also it can be created using plan model.
        response = self.client.post(
            reverse("create"),
                self.invalid_plan_data_payload_1,
                format="json"
        )    
        #print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg="Plan creation failed.")


    def test_api_cannot_create_a_plan_without_valid_amount(self):
        """Test the api has plan creation capability."""
        #Create a plan using API, also it can be created using plan model.
        response = self.client.post(
            reverse("create"),
                self.invalid_plan_data_payload_2,
                format="json"
        )    
        #print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg="Plan creation failed.")


    def test_api_cannot_create_a_plan_without_valid_period(self):
        """Test the api has plan creation capability."""
        #Create a plan using API, also it can be created using plan model.
        response = self.client.post(
            reverse("create"),
                self.invalid_plan_data_payload_3,
                format="json"
        )    
        #print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg="Plan creation failed.")



    def test_api_can_get_plans(self):
        """Test the api fetch plans."""
        #Again creating plan to make this test independent, it seems
        #Test DB is destroyed before this test can fetch the created object.
        new_plan = Plan(
                        plan_name="Monthly", 
                        description="This is test description",
                        amount=99,
                        currency="INR",
                        period= "monthly",
                        interval= 1,
                        notes="Test Notes"
                    )
        new_plan.save()
        new_response = self.client.get(
            reverse("list"),
            content_type="application/json"
        ) 

        response_dict = json.loads(new_response.content)
        self.assertEqual(new_response.status_code, status.HTTP_200_OK, msg="Fetching Plans Failed")
        self.assertIs((len(response_dict)>0),True, msg="Fetching Plans Failed")

    def test_api_can_get_plan(self):
        """Test the api fetch a given plan (by id)."""
        #Again creating plan to make this test independent, it seems
        #Test DB is destroyed before this test can fetch the created object.
        new_plan = Plan(
                        plan_name="Monthly", 
                        description="This is test description",
                        amount=99,
                        currency="INR",
                        period= "monthly",
                        interval= 1,
                        notes="Test Notes"
                    )
        new_plan.save()
        new_response = self.client.get(
            reverse("listone", kwargs={'pk':new_plan.pk}),
            content_type="application/json"
        ) 

        response_dict = json.loads(new_response.content)
        self.assertEqual(new_response.status_code, status.HTTP_200_OK, msg="Fetching Plans Failed")
        self.assertIs((len(response_dict)>0),True, msg="Fetching Plans Failed")
        
    def test_api_can_update_plan(self):
        """Test the api update plans."""
        #Again creating plan to make this test independent, it seems
        #Test DB is destroyed before this test can fetch the created object.
        new_plan = Plan(
                        plan_name="Monthly Test PUT Request", 
                        description="This is test description",
                        amount=99,
                        currency="INR",
                        period= "monthly",
                        interval= 1,
                        notes="Test Notes"
                    )
        new_plan.save()
        new_plan.refresh_from_db()
        #print(new_plan.plan_name)

        new_response = self.client.put(
            reverse("update", kwargs={'pk':new_plan.pk}),
            self.valid_plan_data_payload,
            format="json"
        ) 
        self.assertEqual(new_response.status_code, status.HTTP_200_OK, msg="Update Plan Failed")
        try:
            updatedObjName = Plan.objects.get(plan_name=self.valid_plan_data_payload.get("plan_name"))
        except Plan.DoesNotExist:
            updatedObjName = None
        self.assertIsNotNone(updatedObjName)

    