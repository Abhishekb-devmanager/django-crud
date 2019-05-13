from django.contrib import admin

# Register your models here.
from .models import Plan
from .models import PlanFeature
admin.site.register(Plan)
admin.site.register(PlanFeature)