# lostfound_app/forms.py
from django import forms
from .models import LostItem, Claim

class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = ['title', 'description', 'location', 'image']

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['claim_message']
