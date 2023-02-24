from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
import datetime


class User(AbstractUser):
    pass

class Category(models.Model):
    FASHION = 'F'
    TOYS = 'T'
    ELECTRONICS = 'E'
    HOME = 'H'
    OTHERS = 'O'
    CATEGORIES = [
        (FASHION, 'Fashion'),
        (TOYS, 'Toys'),
        (ELECTRONICS, 'Electronics'),
        (HOME, 'Home'),
        (OTHERS, 'Others')
    ]
    category_type = models.CharField(max_length=1, choices=CATEGORIES, default=FASHION)

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner")
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=1000)
    photo_url = models.URLField(max_length=500)
    starting_bid = models.IntegerField(validators=[MinValueValidator(1)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_listing")
    date = models.DateField(default=datetime.date.today, null=True)
    
    def __str__(self):
        return f"Title: {self.title}; ID: {self.id}"
    
class Bid(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_owner", null=True)
    value = models.IntegerField(validators=[MinValueValidator(1)], null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bid", null=True)
    date = models.DateField(default=datetime.date.today, null=True)
    
class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_owner", null=True)
    content = models.CharField(max_length=2500, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comment", null=True)
    date = models.DateTimeField(default=datetime.date.today, null=True)
    
class Watchlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_owner", null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_watchlist", null=True)
    