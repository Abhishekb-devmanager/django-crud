from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PlanView
from .views import PlanFeatureView
#from .views import DetailsPlanView 

urlpatterns = [
    url(r'^plans/$', PlanView.as_view(), name="list"),
    url(r'^plan/(?P<pk>\d+)', PlanView.as_view(), name="listone"),
    url(r'^plans/$', PlanView.as_view(), name="create"),
    url(r'^plan/(?P<pk>\d+)$', PlanView.as_view(), name="update"),
    url(r'^plan/(?P<pk>\d+)/features', PlanFeatureView.as_view(), name="plan_feature_list"),
    url(r'^features/$', PlanFeatureView.as_view(), name="plan_feature_list")
]

urlpatterns = format_suffix_patterns(urlpatterns)
