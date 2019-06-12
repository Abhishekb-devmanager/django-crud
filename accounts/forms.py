from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

class UserAdminCreationForm(forms.ModelForm):
#     """A form for creating new users. Includes all the required
#     fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        
        # REMOVING PHONE NO ABILITY FROM ADMIN FOR NOW 6th June
        #TODO: Add it again
        #user.phone_no = self.cleaned_data["phone_no"]

        # validation logic should be in models so that it is tied with the core business logic a
        # and not scattered throughout the code in forms. #

        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (#'first_name', 
                  #'last_name', 
                  'email', 
                  #REMOVING PHONE NO ABILITY FROM ADMIN FOR NOW 6th June
                  #TODO: Add it again
                  #'phone_no',
                  'active',
                  'admin',
                  'reader',
                  'staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]