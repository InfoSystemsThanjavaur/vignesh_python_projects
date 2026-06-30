"""
URL configuration for bank project.

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
from django.urls import path,include
from home import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
   path('',views.home,name=""),

   path('adlogin.html',views.admin,name='adlogin'),
   path('adreg.html',views.adreg,name='adreg'),
   
   path('bd.html',views.bankdetail,name="bankdetail"),
   path('remove.html',views.remove,name="remove"),
   
   path('cardreg.html',views.apply,name='apply'),
   path('check.html',views. predict_fraud,name='check'),
   

   path('user.html',views.user,name='user'),
    path('userreg.html',views.userreg,name='register'),
  
   path('transfer.html',views.transfer,name='transfer'),
   path('ViewTransactions.html',views.viewTransaction,name='viewTransaction'),
   path('udetail.html',views.detail,name='detail'),
   
   path('home.html',views.logout,name='logout'),
   path('contact.html',views.contact,name='contact'),
   path('about.html',views.about,name='about'),
   
   
   
   
  
   path('admin.html',views.ad,name='ad'),

   path('ViewTransactions.html',views.viewTransaction,name='transfer_details'),
   path('ViewTransactions.html/download/',views.download,name='download')


]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)