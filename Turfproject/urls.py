
from django.contrib import admin
from django.urls import path,include

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('credentials/',include('credentials.urls')),
    path('bookings/',include('booking.urls')),

    path('',include('customer.urls')),
    path('owner/',include('turfowner.urls')),

]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()