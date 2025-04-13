from django.contrib import admin
from .models import turf_table,reviewtable



class TurfTableAdmin(admin.ModelAdmin):
    # Define the fields to display in the table
    list_display = ('name', 'ownername', 'game_type', 'location', 'open_time', 'close_time', 'rent', 'closed')

    # Optionally, you can add filters to make it easier to search through data
    list_filter = ('game_type', 'closed', 'ownername')

    # Add search functionality (optional)
    search_fields = ('name', 'location', 'ownername__username')

    # Add ordering (optional)
    ordering = ('name',)  # You can change it to any field you'd like

    # Optionally, specify the fields that are editable directly from the list view
    list_editable = ('closed',)

# Register the model and the custom admin class
admin.site.register(turf_table, TurfTableAdmin)



class ReviewTableAdmin(admin.ModelAdmin):
    # Display the necessary fields in the list view
    list_display = ('name', 'email', 'turf', 'message')


    # Optionally, add search functionality
    search_fields = ('name', 'email', 'message', 'turf__name')

    # Optionally, specify the fields that are editable directly from the list view
    list_editable = ('message',)


   
# Register the model and the custom admin class
admin.site.register(reviewtable, ReviewTableAdmin)

