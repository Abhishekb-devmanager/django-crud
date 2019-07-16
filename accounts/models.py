from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager,AbstractBaseUser
)
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token

class GuestEmail(models.Model):
    email      = models.EmailField(
                    verbose_name = 'email address', 
                    max_length = 255, 
                    unique=True
                )
    is_active = models.BooleanField(default=True)
    modified_at = models.DateTimeField(
        verbose_name ='date modified',
        auto_now_add=True, 
        help_text="email last updated on")

    def __str__(self):
        return self.email
    


class UserManager(BaseUserManager):
    def create_user(self, email, phone_no=None, password=None, is_admin = False, is_reader = False, is_active = True):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        #View will ensure that an email is autogenerated in case only phone no is provided.
        user_obj = self.model(
            email=self.normalize_email(email),
        )
        #user_obj.phone_no = phone_no
        # user_obj.admin = is_admin
        # user_obj.reader = is_reader
        # user_obj.active = is_active
        user_obj.is_admin = is_admin
        user_obj.is_reader = is_reader
        user_obj.is_active = is_active
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        
        try:
            if phone_no is not None:
                phone = UserPhone(User=user_obj, phone_no=phone_no)
                phone.save
        except:
            pass
        Token.objects.create(user=user_obj)
        return user_obj

    #def create_superuser(self, email, date_of_birth, password):
    #def create_superuser(self, phone_no, email, password):
    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            #phone_no,
            password=password,
            is_admin = True,
            is_reader=True,
            is_active= True
        )
        return user

class UserPhone(models.Model):
    phone_no   = PhoneNumberField(unique=True)
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='user_phone',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    created_at = models.DateTimeField(
        verbose_name ='date created',
        auto_now_add=True, 
        help_text="Phone added on")

    modified_at = models.DateTimeField(
        verbose_name ='date modified',
        auto_now_add=True, 
        help_text="Phone last updated on") 

    def __str__(self):
        return str(self.phone_no)
    

class User(AbstractBaseUser, PermissionsMixin):
    email      = models.EmailField(
                    verbose_name = 'email address', 
                    max_length = 255,
                    unique=True
                ) 
    date_joined = models.DateTimeField(verbose_name ='date joined', auto_now_add=True)
    # active = models.BooleanField(default=True)
    # admin = models.BooleanField(default=False)
    # reader = models.BooleanField(default=True)
    # staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_reader = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    modified_at = models.DateTimeField(verbose_name ='date modified',auto_now=True, help_text="Time when this is modified on admin panel - to be entered")
    created_at= models.DateTimeField(auto_now_add=True, help_text="Time when it was created on admin panel")

    objects = UserManager()

    USERNAME_FIELD = 'email' 
    # let me remove phone no from REQUIRED_FIELDS 
    # Admin or terminal will not allow user creation with phone no.
    #REQUIRED_FIELDS = ['phone_no'] #only impacts creation of superuser
    

    # class Meta:
    #      db_table = 'auth_user'

    def __str__(self):
        if self.email:
            return self.email
        
    def has_related_object(self):
        has_user_phone = False
        try:
            has_user_phone = (self.user_phone is not None)
        except UserPhone.DoesNotExist:
            pass
        return has_user_phone
            
    def clean(self):
        if not self.email:
            if not self.phone_no:
                raise ValidationError('A valid email or phone number is required for us to identify you.')

        if not self.phone_no:
            if not self.email:
                raise ValidationError('A valid email or phone number is required for us to identify you.')


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # def get_full_name(self):
    #     return self.first_name + self.last_name
    
    # @property
    # def is_admin(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.admin

    # @property
    # def is_reader(self):
    #     "Is the user a reader?"
    #     # Simplest possible answer: All admins are staff
    #     return self.reader

    # @property
    # def is_active(self):
    #     "Is the user active?"
    #     # Simplest possible answer: All admins are staff
    #     return self.active

    # @property
    # def is_staff(self):
    #     "Is the user active?"
    #     # Simplest possible answer: All admins are staff
    #     return self.staff

    