from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm

from .models import User, GuestEmail

class CustomUserAdmin(UserAdmin):

    # The forms to add and change user instances
    add_form = UserAdminCreationForm
    #form = UserAdminChangeForm

    readonly_fields = ('full_name','date_joined')

    #NOTE: You can define a function to return fullname using instance.
    def full_name(self, instance):
        fullname = [instance.first_name, instance.last_name]
        return " ".join(fullname)

    #https://stackoverflow.com/questions/163823/can-list-display-in-a-django-modeladmin-display-attributes-of-foreignkey-field/3351431#3351431
    def get_phone_no(self, instance):
        phn = instance.phone_no
        print(phn)
        return phn
    
    # def get_queryset(self, request):
    #     return super().get_queryset(request).select_related('phone_no')
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email','get_phone_no','date_joined', 'is_admin')
    list_filter = ('is_admin','is_reader')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name','date_joined')}), #full_name callable
        ('Permissions', {'fields': ('is_admin','is_reader','is_staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    # # search_fields = ('email', 'phone_no')
    search_fields = ('email',)
    # # ordering = ('email', 'phone_no')
    # search_fields = ('email', 'User__phone_no')
    ordering = ('email',)
    #User.admin_order_field = 'user__phone_no'
    
    filter_horizontal = ()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
admin.site.register(GuestEmail)
admin.site.register(User, CustomUserAdmin)


