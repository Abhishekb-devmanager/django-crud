# django-crud

- AbstractBaseUser provides the minimal and vital user object
- Model gets picked from the settings 
- Each application can extend the Custom User model and implement required details however queries would then need to use JOIN operation to fetch which has performance impact
- User model should be defined early in the project because user serves as foreign key to a lot of tables created during the development, changing the user model again would need the change across tables. This may need 
    - dropping of the current tables
    - running initial migration once again
    - repopulation of data 
        - Fixture will come to rescue for exporting data from the tables for each app in json format and then repopulating the data into the freshly created tables.
        - Extermely dangerous approach for production environment. Should be planned and tested carefully.
    - so why to invite this much of a hassle if we can make sure we define the minimal mandatory attributes of user object and then extend many available options to extend the user model
- Capturing Email and phone number with user id into a separate table is a good idea, this will allow us to scale the most crucial data points connected to a user 
    - this will need a separate model to be defined for Email, Phone number or attributes of similar importance.
    - Another way to handle this is to create a guest user with email as an attribute.
- Admin.py - UserAdmin class form settings are mandatory to be overridded, to provide an input to the base implementation. so missing the fieldsets implementation or search will lead to a django exception. the base implementation looks for username it is you need to tell in admin.py.
