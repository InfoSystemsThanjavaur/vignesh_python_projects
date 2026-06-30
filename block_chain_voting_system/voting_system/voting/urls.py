from django.urls import path
from . import views

urlpatterns = [
path('', views.home, name='home'),
path('about/', views.about, name='about'),
    path('vote/', views.vote, name='vote'),
    path('results/', views.results, name='results'),
    path('register/', views.register_view, name='register'),
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
path('', views.login_view),
path('download-report/', views.download_report, name='download_report'),
]