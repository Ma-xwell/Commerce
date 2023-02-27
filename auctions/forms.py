from django import forms
from django.core.validators import MinValueValidator
from .models import Category

class ListingForm(forms.Form):
    title = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'formelement'}))
    content = forms.CharField(max_length=1000, required=True, widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'formdescription'}))
    photo_url = forms.URLField(max_length=500, required=False, widget=forms.URLInput(attrs={'placeholder': 'Photo URL (optional)', 'class': 'formelement', 'class': 'formelement'}))
    starting_bid = forms.FloatField(validators=[MinValueValidator(0.1)], min_value=0, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Initial price', 'step': '0.1', 'class': 'formelement'}))
    category = forms.ChoiceField(choices=Category.CATEGORIES, widget=forms.Select(attrs={'class': 'formelement'}))
    
class CommentForm(forms.Form):
    content = forms.CharField(label="", max_length=2500, widget=forms.TextInput(attrs={'placeholder': 'Your comment', 'class': 'formelement'}))