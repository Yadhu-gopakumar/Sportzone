
from django.urls import path
from . import views
urlpatterns = [
    path('',view=views.ownerhome,name='ownerhome'),
    path('ownersearchturf',views.ownersearchturf,name='ownersearchturf'),
    path('addturf',views.addturf,name='addturf'),
    path('deleteTurf/<int:id>/',views.deleteTurf,name='deleteTurf'),
    path('editTurf/<int:id>/',views.editTurf,name='editTurf'),
    path('changeslots/<int:id>/',views.changeslots,name='changeslots'),
    path('allbookings',views.allbookings,name='allbookings'),
    path('turfbookings/<int:id>/',views.turfbookings,name='turfbookings'),
    path('addreview/<int:id>/',views.addreview,name='addreview'),
    path('played/<str:start_time>/<int:bid>/<str:user_id>/',views.playedstatus,name='playedstatus')


]