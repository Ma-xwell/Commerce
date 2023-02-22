from django import forms
from django.core.validators import MinValueValidator
from .models import Category

class ListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50)
    content = forms.CharField(label="Content", max_length=1000)
    photo_url = forms.URLField(label="Photo's URL", max_length=500, required=False)
    starting_bid = forms.IntegerField(label="Starting Bid", validators=[MinValueValidator(1)])
    category = forms.ChoiceField(label="Category", choices=Category.CATEGORIES)