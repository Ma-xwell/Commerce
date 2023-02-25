from django import forms
from django.core.validators import MinValueValidator
from .models import Category

class ListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50, required=True)
    content = forms.CharField(label="Content", max_length=1000, required=True)
    photo_url = forms.URLField(label="Photo's URL", max_length=500, required=False)
    starting_bid = forms.FloatField(label="Starting Bid", validators=[MinValueValidator(1)], required=True)
    category = forms.ChoiceField(label="Category", choices=Category.CATEGORIES)
    
class CommentForm(forms.Form):
    content = forms.CharField(label="Your comment", max_length=2500)