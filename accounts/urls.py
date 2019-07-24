from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views_auth import CustomAuthToken
from .views_guest import GuestUserView
from .views import UserView


#from .views import views

urlpatterns = [
    url(r'^users/$', UserView.as_view(), name="listuser"),
    url(r'^user/(?P<pk>\d+)', UserView.as_view(), name="oneuser"),
    url(r'^users/$', UserView.as_view(), name="adduser"), #repeating to identify 2 diff functions
    url(r'^user/(?P<pk>\d+)$', UserView.as_view(), name="updateuser"),
    #url(r'^user/(?P<pk>\d+)/profile', UserProfile.as_view(), name="plan_feature_list")
    url(r'^api-token-auth/', CustomAuthToken.as_view(), name="authenticate"),
    url(r'^signup', GuestUserView.as_view(), name='usersignup')
]

urlpatterns = format_suffix_patterns(urlpatterns)
