from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    NOCATEGORY = "NO"
    FASHION = 'F'
    TOYS = 'T'
    ELECTRONICS = 'E'
    HOME = 'H'
    OTHERS = 'O'
    CATEGORIES = [
        (NOCATEGORY, "No category"),
        (FASHION, 'Fashion'),
        (TOYS, 'Toys'),
        (ELECTRONICS, 'Electronics'),
        (HOME, 'Home'),
        (OTHERS, 'Others')
    ]
    category_type = models.CharField(max_length=2, choices=CATEGORIES, default=FASHION)
    
    def __str__(self):
        return f"{self.category_type}"

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner")
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=1000)
    photo_url = models.URLField(max_length=500, null=True)
    starting_bid = models.FloatField(validators=[MinValueValidator(1)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_listing")
    date = models.DateTimeField(default=timezone.now, null=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Title: {self.title}; ID: {self.id}"
    
class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_owner", null=True)
    value = models.FloatField(validators=[MinValueValidator(1)], null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bid", null=True)
    date = models.DateField(default=timezone.now, null=True)
    
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_owner", null=True)
    content = models.CharField(max_length=2500, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comment", null=True)
    date = models.DateTimeField(default=timezone.now, null=True)
    
class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_owner", null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_watchlist", null=True)
    
class Winner(models.Model):
    id = models.AutoField(primary_key=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_won", null=True)