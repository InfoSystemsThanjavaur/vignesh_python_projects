"""
URL configuration for smart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from home import views

urlpatterns = [
    path("",views.home,name=""),
    path("register/", views.register, name="register"),   # Register Page
    path("login/", views.login, name="login"),   # Login Page
    path("dashboard/", views.dashboard, name="dashboard"),   # Dashboard Page
    path("logout/", views.logout_view, name="logout"), 
     path('weather/', views.weather_details, name='weather_details'),
         path('soil-analysis/', views.soil_analysis, name='soil_analysis'),
          path('crop-recommendation/', views.crop_recommendation, name='crop_recommendation'),
          path('analytics-reports/', views.analytics_reports, name='analytics_reports'),# Logout
          path('agri-support/', views.agri_support, name='agri_support'),
    path("download-excel/", views.download_excel, name="download_excel"),
]
