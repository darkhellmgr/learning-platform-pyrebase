from django.urls import path
from mainapp import views

urlpatterns = [
    path('sign/', views.sign, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('postsign/', views.postsign, name='admin'),
    path('details/', views.details),
    path('allform/<str:formtype>/', views.allform,name='allform'),
    path('allform/<str:formtype>/<str:id>', views.allform,name='allform'),
    path('home/', views.home, name='home'),
    path('userform/<str:formtype>/', views.userform, name='userform'),


]