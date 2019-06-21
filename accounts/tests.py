from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from .models import User, UserPhone
from phonenumber_field.phonenumber import PhoneNumber
from django.contrib.sites.shortcuts import get_current_site
import json

# Create your tests here.
class UserModelTestCase(TestCase):
    """This class defines the test suite for the Plans model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.user = User(
                        email="abhishekb.bansal@devmanager.com",
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
        self.assertGreater(new_count, old_count, msg= "User created successfully.")

class UserViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
         #fresh plan object created.
        self.user_data = {
                            "email":"akm@gmail.com",
                            "phone_no":"+919192949596",
                            "password":"Pass@123",
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
                                            "user_phone":{"phone_no":"+919899093440"},
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
        responseJson = json.loads(response.content)
        print(responseJson)
        # self.assertContains(
        #                 response, 
        #                 self.user_data.get('email'), 
        #                 status_code=201
        #             )
        if responseJson.get('errors', None) is not None:    
            self.assertEqual(
                    response.status_code, 
                    status.HTTP_201_CREATED, 
                    msg='{}-{}'.format(responseJson['errors'],"User creating failed")
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
        responseJson = json.loads(response.content)
        #print(json.loads(response.content))
        self.assertEqual(
                response.status_code, 
                status.HTTP_201_CREATED, 
                msg="User without email but phone only - creation failed."
            )
        current_site = get_current_site(self.client.request).domain
        phn = self.user_data_without_email.get('phone_no')
        autogenerated_email = "{}@{}".format(phn,current_site)
        self.assertEqual(
                responseJson['users']['email'], 
                autogenerated_email, 
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
            msg="User creation succesful even with a short pwd."
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
            email="e@get.com",
            password="Pass@123"
        )
        new_user.save()
        user_phn = UserPhone(phone_no="+918999833333", owner=new_user)
        user_phn.save()
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
        user_phn = UserPhone(phone_no="+918989833333", owner=new_user)
        user_phn.save()

        new_response = self.client.get(
            reverse("oneuser", kwargs={'pk':new_user.pk}),
            content_type="application/json"
        ) 

        response_dict = json.loads(new_response.content)
        #print(response_dict)
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
        """Test the api update user phone no."""

        #Critical to check if user has email, can he add phone no later?
        new_user = User(
            email="update@update.com", 
            password="Pass@123"
        )
        new_user.save()
        new_user.refresh_from_db()

        updated_phn = {
            "email":new_user.email,
            "phone_no":"+919899083458",
            "password":new_user.password
        } 
        new_response = self.client.put(
            reverse(
                "updateuser", 
                kwargs={'pk':new_user.pk}),
                updated_phn,
                format="json"
            ) 
        responseJson = json.loads(new_response.content)
        print(responseJson)
        if responseJson.get('errors', None) is not None:    
            self.assertEqual(
                    new_response.status_code, 
                    status.HTTP_200_OK, 
                    msg='{}-{}'.format(responseJson['errors'],"User phoneno update Failed")
                )
    
        #related name is the name of reverse relationship from user to userphone
        #if specified it disable the default name of related name userphone_set or userphone.
        updatedObjName = new_user.user_phone
        self.assertEqual(
                            updatedObjName.phone_no,
                            updated_phn['phone_no'],
                            msg="User with {} failed to update with ph {}".format(new_user.email,updatedObjName.phone_no)
                        )
        #testOnj1 = new_user.userphone_set.all()
        #testOnj2 = new_user.userphone.all()
        #print(updatedObjName.phone_no)
        #print(updatedObjName.owner)
        #print(testOnj1)
        #print(testOnj2)
        # print(hasattr(new_user, 'userphone'))
        # print(hasattr(new_user, 'user_phone'))
        # print(hasattr(new_user, 'userphone_set'))






    def test_api_can_update_user_email_later(self):
        """Test the api update user email later."""

        #create a new user using model       
        new_user = User(
            email="+919899023453@example.com",
            password="Pass@123"
        ) #without email
        new_user.save()
        new_phone = UserPhone(owner=new_user, phone_no="+919899023453")
        new_phone.save()
        new_user.refresh_from_db()

        updated_email = {
                    "email":"raja@k.com",
                    "password":"Pass@123"
            } 
        new_response = self.client.put(
            reverse(
                "updateuser", 
                kwargs={'pk':new_user.pk}),
                updated_email,
                format="json"
            ) 
        responseJson = json.loads(new_response.content)
        if responseJson.get('errors', None) is not None:    
            self.assertEqual(
                    new_response.status_code, 
                    status.HTTP_200_OK, 
                    msg='{}-{}'.format(responseJson['errors'],"User email update Failed")
                )
        
        # self.assertEqual(
        #     new_response.status_code, 
        #     status.HTTP_200_OK, 
        #     msg="Updated User email Failed"
        # )
        try:
            updatedObjName = User.objects.get(email=updated_email.get("email"))
        except User.DoesNotExist:
            updatedObjName = None
        self.assertIsNotNone(updatedObjName)
