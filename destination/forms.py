from django import forms

from django.contrib.auth import get_user_model
from .models import Destination

User=get_user_model()

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields=(
            'place_name',
            'place_description',
            'place_picture',
            'place_status'
        )