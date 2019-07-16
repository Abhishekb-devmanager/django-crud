"""accounts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
#from django.urls import include, path  # For django versions from 2.0 and up
from django.urls import include, path, re_path
from django.views.generic.base import TemplateView # new

urlpatterns = [
    # default page 
    path('', include('accounts.urls')),
    path('', include('plans.urls')),
    path('plans/', include('plans.urls')),
    path('users/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # new
    path('', TemplateView.as_view(template_name='home.html'), name='home'), # new

    #re_path(r'^', include('plans.urls')) ,
    #re_path(r'^', include('accounts.urls'))
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns