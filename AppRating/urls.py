"""PoseDetection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from Users import views
from Admins import views as adv
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users
    path('', views.base, name='base'),
    path('Userlogin', views.Userlogin, name='Userlogin'),
    path('Userregister/', views.UserRegister, name='Userregister'),
    path('UserHome/', views.UserHome, name='UserHome'),
    path('Datasetview/', views.DatasetView, name='Datasetview'),
    path('training/', views.training, name='training'),
    path('predict/', views.Predication, name='predict'),
    #Admin
    path('AdminLogin/', adv.AdminLogin, name='AdminLogin'),
    path('AdminHome/', adv.AdminHome, name='AdminHome'),
    path('viewusers/', adv.viewusers, name='viewusers'),
    path('Activateusers//<int:uid>/', adv.activate_user, name='Activateusers'),
    path('Deactivateusers/', adv.Deactivateusers, name='Deactivateusers'),
    path('Deleteusers/', adv.delete_user, name='Deleteusers'),
] +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
