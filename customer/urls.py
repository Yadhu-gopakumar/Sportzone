from django.urls import path
from . import views


urlpatterns = [
        path('', views.userhome,name='userhome'), 
        path('viewturflist',views.viewturflist,name="viewturflist"),
        path('searchturf',views.searchturf,name="searchturf"),
        path('userbookings',views.userbookings,name='userbooking'),
        path('turf/<int:turf_id>/available_slots/', views.available_slots, name='available_slots'),
        path('download_ticket/<int:booking_id>/', views.download_ticket, name='download_ticket'),
      ]