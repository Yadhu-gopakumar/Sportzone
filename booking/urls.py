from django.urls import path
from . import views


urlpatterns = [
       path('bookslots/<int:id>/',views.bookslots,name='bookslots'),
       path('userbookings',views.userbookings,name='userbookings'),
       path('cancelbooking/<int:bid>/<int:tid>/',views.cancelbooking,name='cancelbooking'),
       path('addname/<int:bid>/',views.addname, name='addname'),
       path('payment/success/', views.payment_success, name='payment_success'),
        
]