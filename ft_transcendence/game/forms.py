from django import forms
from .models import Player

class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['display_name', 'avatar']

