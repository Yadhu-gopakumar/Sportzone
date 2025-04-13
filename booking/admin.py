

from django.contrib import admin
from .models import BookingSlotTable, UserBookingTable

class BookingSlotTableAdmin(admin.ModelAdmin):
    list_display = ('turf', 'booking_date', 'expired')
    list_filter = ('turf', 'expired')
    search_fields = ('turf__name', 'booking_date')

class UserBookingTableAdmin(admin.ModelAdmin):
    list_display = ('customer', 'turfname', 'amount', 'booking_date', 'expired')
    list_filter = ('customer', 'turfname', 'expired')
    search_fields = ('customer__username', 'turfname__name', 'booking_date')

admin.site.register(BookingSlotTable, BookingSlotTableAdmin)
admin.site.register(UserBookingTable, UserBookingTableAdmin)
