from django.db import models

# Create your models here.
class Plan(models.Model):
    platform_plan_id =  models.CharField(max_length=20,blank=True, help_text="Plan Id returned from RazorPay")
    entity_type=models.CharField(max_length=10, blank=True,help_text="Looking at plan response from API - matching to type key")
    plan_name = models.CharField(max_length=300, help_text="Business name of the plan")
    description = models.TextField(help_text="Feature description of the plan")
    amount = models.IntegerField(help_text="Price of the plan")
    currency = models.CharField(max_length=3, help_text="Should be INR")
    period = models.CharField(max_length=7, help_text="If customer is charged every 2 months then this value should be monthly")
    interval = models.IntegerField(help_text="If customer is charged every 2 months then this value should be 2")
    notes = models.CharField(max_length=300, blank=True, help_text="This can be converted to a custom object later as key value pairings")
    modified_at = models.DateTimeField('date published',auto_now=True, help_text="Time when this is modified on admin panel - to be entered")
    created_at= models.DateTimeField(auto_now_add=True, help_text="Time when it was created on admin panel")

    class Meta:
        db_table = 'plans'

    def __str__(self):
        return self.plan_name

class PlanFeature(models.Model):
    #added blank true to fix plan field required error while submitting. Serializer.isvalid failed w/o.
    plan = models.ForeignKey(Plan,related_name="features", on_delete=models.CASCADE)
    display_text = models.CharField(max_length=500, help_text="Feature description displayed on plan page")
    created_at= models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'plan_features'
    
    def __str__(self):
        return self.display_text

