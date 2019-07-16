# django-crud

- AbstractBaseUser provides the minimal and vital user object
- Model gets picked from the settings 
- Each application can extend the Custom User model and implement required details however queries would then need to use JOIN operation to fetch which has performance impact
- User model should be defined early in the project because user serves as foreign key to a lot of tables created during the development, changing the user model again would need the change across tables. This may need 
    - dropping of the current tables
    - running initial migration once again
    - repopulation of data 
        - "Fixture" will come to rescue for exporting data from the tables for each app in json format and then repopulating the data into the freshly created tables.
        - Extermely dangerous approach for production environment. Should be planned and tested carefully.
    - so why to invite this much of a hassle if we can make sure we define the minimal mandatory attributes of user object and then extend using many available options to extend the user model
- Capturing Email and phone number with user id into a separate table is a good idea, this will allow us to scale the most crucial data points connected to a user 
    - this will need a separate model to be defined for Email, Phone number or attributes of similar importance. 
    - This is done defining onetoone relationship - defined owner ie user as a one to one relationship in UserPhone model (separate table)
    - OnetoOne relationship should define the "related_name" attribute. The value needs to be added to the field list. user_phone in this case. When I did not defined this Django was using phone_no as primary key to match with a existing phone no in the UserPhone table while creating the user in serializer, is_valid failed with a validation error, a phone no with the "+9188438723973" does not exist, also it need to select the phone no from drop down to assign it to user. (#TODO: Admin form is still untested)
    - While defining the user model I tried to put phone_id in user table and user_id in phone table to be able to retreive phone no or user info from either models. It successfully created the tables but needed to create the user before a phone could exist and phone_no while creating the user. so it is kind of cyclic dependency specifying. We want phone no to be saved at the same time as a user is created. I removed phone_id from user because we want to save phone no or email before anything. Related_name automatically allowed reverse retrieval or phone from user. (#TODO: Docs but need to test)
    - Another way to handle this is to create a guest user with email as an attribute. 
    - Nested serializers is used to be able save, retrieve (send response) phone along with user object along with onetoone relationship
- During customizing the Django User model, create_user, create_superuser need to be defined as mandatory functions to be overridden under the mandatory UserManager class. UserManager is assigned to model "objects" which is the defualt manager otherwise.
- Customizing Error responses: DRF needs to define custom_exception_handler with keys you need in the response to detail out error. https://www.django-rest-framework.org/api-guide/exceptions/
- APIException is extended to customize error structure in response. Custom exceptions are defined as subclasses of APIException class and raised as exceptions in the try:except:raise: block. Django will use the customexception class to generate error responses. Define additional error keys to response in this class.
- Authentication
    - Create token as soon as user is created (signs up)
        - Request is handled by a fresh view_auth.py which extending ObtainAuthToken, with custome serializer to accept emails. No model is connected with Serializer. Its not a model serializer.
        - Simply used the user model to create token when user created - no post_save hooks used
        - I misunderstood settings.py - AUTHENTICATION_BACKENDS vs DEFAULT_AUTHENTICATION_CLASSES
        - AUTHENTICATION_BACKENDS - when I want email instead of username, I had write a custom authenticate method to override baseauth's and session auth's authenticate method and declare it as my custom backen in settings.
        - DEFAULT_AUTHENTICATION_CLASSES - are declared then they will call the authenticate method on every API call hitting and returns the authorised user.
        - Also misinterpreted that while declaring the serializer - I need to declare permission classes and authetication class on the top but this was not needed. Our custom field email and password needs to be freshly declared in the serializer.
        - For a long time - returning tuple from authenticate method containing user object and token kept throwing error that tuple does not contains a backend attribute because the authenticate in __init.py__ annotates the user.backend = path of backend which was used to authenticate the credentials.
        - Current two backends are configured - Custom and ModelBackend. ModelBackend is not playing any role here but it was configured by default so I have not removed it yet, seems like it will be used for admin panel.

    - Implement login api which take email and password, matched in db
    - Return token thus generated
    - Protect the Plan api with authentication - only logged in users gets to see the plan listing
        - Define authentication_classes (Token Auth in this case) and permission_classes (IsAuthenticated) on top of the view or on top function
    - Users with is_admin TRUE will get access to plan creation and update abilities.
    - GET function is available to all users
    - POST, PUT, DELETE Protected for only admin users which is the superuser
    - Protected by using Method Decorators and user_passes_test decorator. Method decorator converts a function decoratore to method decorator for use in Class based views.

- Admin.py - UserAdmin class form settings are mandatory to be overridded, to provide an input to the base implementation. so missing the fieldsets implementation or search will lead to a django exception. the base implementation looks for username it is you need to tell in admin.py.
