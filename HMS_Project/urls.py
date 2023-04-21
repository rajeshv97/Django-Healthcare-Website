"""HMS_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from accounts import views
from django.urls import path,include
from django.contrib.auth import views as auth_views
from accounts import views as acc_views
from dashboard import views as dash_view
from django.contrib import admin

admin.site.site_header = 'Wildcat Healthcare'                    # default: "Django Administration"
admin.site.index_title = 'Wildcat Healthcare'                 # default: "Site administration"
admin.site.site_title = 'Wildcat Healthcare' # default: "Django site admin"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('',include('dashboard.urls')),
    path('login/',auth_views.LoginView.as_view(template_name = 'accounts/login.html'),name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'accounts/logout.html'),name = 'logout'),
    path('registerpatient/', acc_views.registerpatient, name = 'registerpatient'),
    path('patientprofile/', acc_views.patientprofile, name = 'patientprofile'),
    path('employeelogin/',auth_views.LoginView.as_view(template_name = 'accounts/employeelogin.html'),name = 'employeelogin'),
    path('employeelogout/',auth_views.LogoutView.as_view(template_name = 'accounts/employeelogout.html'),name = 'employeelogout'),
    path('employeeprofile/', acc_views.employeeprofile, name = 'employeeprofile'),
   
    
]

