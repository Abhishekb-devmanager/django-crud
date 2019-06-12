from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from .models import User
import json

# Create your tests here.
class UserModelTestCase(TestCase):
    """This class defines the test suite for the Plans model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.user = User(
                        email="abhishekb.bansal@devmanager.com",
                        phone_no="+919899093440",
                        active=1,
                        admin= 1,
                        staff= 1,
                        reader= 1
                    )

    def test_model_can_create_a_user(self):
        """Test the user model can create a plan."""
        old_count = User.objects.count()
        self.user.save()
        new_count = User.objects.count()
        self.assertNotEqual(old_count, new_count)

class UserViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
         #fresh plan object created.
        self.user_data = {
                            "email":"abhishekb.bansal@devmanager.com",
                            "phone_no":"+919899093440",
                            "active": 1,
                            "admin": 0,
                            "staff": 0,
                            "reader": 1
                        }
                         
        #TC should pass when ph is avail but not email
        self.user_data_without_email = {
                                            "email":"",
                                            "phone_no":"+919899093440",
                                            "password":"Pass@123"
                                        }

        self.user_data_without_phoneno = {
                                            "email":"2@gml.com",
                                            "phone_no":"",
                                            "password":"Pass@123"
                                        }

        #TC should pass when ph is avail but not email key 
        #Also check the default values for date joined, admin, staff and reader status.
        #APIs will allow only reader status.
        #Email and phone no is allowed to be changed only by the logged in user
        self.user_data_without_email_key = {
                                            "phone_no":"+919899093440",
                                            "password":"Pass@123"
                                        }

        #TC should fail in case of invalid password (less than 8 chars)
        self.user_data_with_short_pwd = {
                                            "email":"a@g.com",
                                            "password":"qwert"
                                        }
        self.user_data_with_allsmallcase_pwd = {
                                            "email":"a@g.com",
                                            "password":"abhishek"
                                        }

        self.user_data_without_any_key = {}

       
    #TC should pass when ph is avail but not email
    def test_api_can_create_a_user(self):
        """Test the api has User creation capability."""
        #Create a User using API, also it can be created using user model.
        response = self.client.post(
            reverse("adduser"),
            self.user_data,
            format="json"
        )    
        print(json.loads(response.content))
        self.assertEqual(
                response.status_code, 
                status.HTTP_201_CREATED, 
                msg="User creation failed."
            )
        self.assertContains(
                        response, 
                        self.user_data.get('email'), 
                        status_code=201
                    )

        
    #TC should pass with email but without phone no
    def test_api_can_create_a_user_with_email_only(self):
        """Test the api has User creation capability with email only."""

        response = self.client.post(
            reverse("adduser"),
            self.user_data_without_phoneno,
            format="json"
        )    
        #print(json.loads(response.content))
        self.assertEqual(
                response.status_code, 
                status.HTTP_201_CREATED, 
                msg="User without phone but email only - creation failed."
            )
        self.assertContains(
                        response, 
                        self.user_data_without_phoneno.get('email'), 
                        status_code=201
                    )

    #TC should pass with phone no but without e
    def test_api_can_create_a_user_with_phone_only(self):
        """Test the api has User creation capability with phone only."""

        response = self.client.post(
            reverse("adduser"),
            self.user_data_without_email,
            format="json"
        )    
        #print(json.loads(response.content))
        self.assertEqual(
                response.status_code, 
                status.HTTP_201_CREATED, 
                msg="User without email but phone only - creation failed."
            )
        self.assertContains(
                        response, 
                        self.user_data_without_email.get('phone_no'), 
                        status_code=201
                    )

    #TC should fail without valid pwd
    def test_api_cannot_create_a_user_with_invalid_pwd_min_len(self):
        """Test the api has User creation capability with phone only."""

        response = self.client.post(
            reverse("adduser"),
            self.user_data_with_short_pwd,
            format="json"
        )    
        self.assertEqual(
            response.status_code, 
            status.HTTP_400_BAD_REQUEST, 
            msg="User creation failed due short pwd."
        )
        self.assertContains(
            response, 
            "8 characters", 
            status_code=400
        )
    
    #TC should fail without valid pwd
    def test_api_cannot_create_a_user_with_invalid_pwd_allsmallcase(self):
        """Test the api has User creation capability with phone only."""

        response = self.client.post(
            reverse("adduser"),
            self.user_data_with_allsmallcase_pwd,
            format="json"
        )    
        self.assertEqual(
                response.status_code, 
                status.HTTP_400_BAD_REQUEST, 
                msg="User creation failed due to small case password.User should have atleast 8 characters, 1 capital letter, 1 number"
            )
        
    #check the default values for date joined, admin, staff and reader status.
    def test_api_cannot_create_a_user_with_empty_payload(self):
        """Test the api has User creation capability with phone only."""

        response = self.client.post(
            reverse("adduser"),
            self.user_data_without_any_key,
            format="json"
        )    
        #print(json.loads(response.content))
        self.assertEqual(
            response.status_code, 
            status.HTTP_400_BAD_REQUEST, 
            msg="Blank user record created."
        )


    def test_api_can_get_users(self):
        """Test the api fetch users."""
        #Again creating user to make this test independent, it seems
        #Test DB is destroyed before this test can fetch the created object.
        new_user = User(
            email="e@get.com"
        )
        new_user.save()
        new_response = self.client.get(
            reverse("listuser"),
            content_type="application/json"
        ) 

        response_dict = json.loads(new_response.content)
        self.assertEqual(
            new_response.status_code, 
            status.HTTP_200_OK, 
            msg="Fetching Users Failed"
        )
        self.assertIs(
            (len(response_dict)>0),
            True, 
            msg="Fetching Users Failed"
        )

    def test_api_can_get_user(self):
        """Test the api fetch a given user (by id)."""
        #Again creating user to make this test independent, it seems
        #Test DB is destroyed before this test can fetch the created object.
        new_user = User(
            email="get@gmail.com",
            password="g3t@laim"
        )
        new_user.save()
        new_response = self.client.get(
            reverse("oneuser", kwargs={'pk':new_user.pk}),
            content_type="application/json"
        ) 

        response_dict = json.loads(new_response.content)
        self.assertEqual(
            new_response.status_code, 
            status.HTTP_200_OK, 
            msg="Fetching Users Failed"
        )
        self.assertIs(
            (len(response_dict)>0),
            True, 
            msg="Fetching Users Failed"
        )
        self.assertContains(
            new_response, 
            "get@gmail.com",
            status_code=200
        )
        
    def test_api_can_update_user_phone(self):
        """Test the api update user."""
        #Again creating user to make this test independent, it seems
        #Test DB is destroyed before this test can fetch the created object.
        new_user = User(
            email="update@update.com", 
            phone_no="+919899023445"
        )
        new_user.save()
        new_user.refresh_from_db()

        updated_phn = {
            "phone_no":"+919899083458",
        } 
        new_response = self.client.put(
            reverse(
                "updateuser", 
                kwargs={'pk':new_user.pk}),
                updated_phn,
                format="json"
            ) 
        self.assertEqual(
            new_response.status_code, 
            status.HTTP_200_OK, 
            msg="Update User Failed"
        )
        try:
            updatedObjName = User.objects.get(phone_no=updated_phn.get("phone_no"))
        except User.DoesNotExist:
            updatedObjName = None
        self.assertIsNotNone(updatedObjName)

    def test_api_can_update_user_email_later(self):
        """Test the api update user email later."""
        #Again creating user to make this test independent, it seems
        #Test DB is destroyed before this test can fetch the created object.
        new_user = User(
            phone_no="+919899023453"
        ) #without email
        new_user.save()
        new_user.refresh_from_db()

        updated_email = {
                    "email":"raja@k.com",
            } 
        new_response = self.client.put(
            reverse(
                "updateuser", 
                kwargs={'pk':new_user.pk}),
                updated_email,
                format="json"
            ) 
        self.assertEqual(
            new_response.status_code, 
            status.HTTP_200_OK, 
            msg="Update User email Failed"
        )
        try:
            updatedObjName = User.objects.get(phone_no=updated_email.get("email"))
        except User.DoesNotExist:
            updatedObjName = None
        self.assertIsNotNone(updatedObjName)
