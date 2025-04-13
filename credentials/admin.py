
from django.contrib import admin
from .models import userprofile, ownerprofile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')

admin.site.register(userprofile, UserProfileAdmin)
admin.site.register(ownerprofile, OwnerProfileAdmin)
