
from django.urls import path
from . import views
urlpatterns = [
    path('userlogin',view=views.userlogin,name='userlogin'),
    path('userregister',view=views.userregister,name='userregister'),
    path('ownerlogin',view=views.ownerlogin,name='ownerlogin'),
    path('ownerregister',view=views.ownerregister,name='ownerregister'),
    path('userlogout',view=views.userlogout,name='userlogout'),
    path('ownerlogout',view=views.ownerlogout,name='ownerlogout'),

]