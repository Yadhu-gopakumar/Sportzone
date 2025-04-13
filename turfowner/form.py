from django import forms
from .models import turf_table

class turfForm(forms.ModelForm):
    class Meta:
        model = turf_table
        fields = ['name', 'game_type', 'location', 'location_url', 'open_time', 'close_time', 'discription',  'rent', 'image']