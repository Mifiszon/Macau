from django import forms
from .models import Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['nick']
        widgets = {
            'nick': forms.TextInput(attrs={
                'placeholder': "Wpisz swój nick",
                'class': 'form-control form-control-lg',
                'aria-label': 'Nick gracza',
                'autocomplete': 'off',
            }),
        }
        labels = {
            'nick': "Twój Nick"
        }
