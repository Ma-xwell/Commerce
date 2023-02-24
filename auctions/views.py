from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import ListingForm, CommentForm
from .models import User, Listing, Category, Bid, Comment, Watchlist
import datetime


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "bid": Bid.objects.order_by('value')
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def createlisting(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            photo_url = form.cleaned_data['photo_url']
            starting_bid = form.cleaned_data['starting_bid']
            category_type = form.cleaned_data['category']
            category = Category.objects.get(category_type=category_type)
            newListing = Listing(owner=user, title=title, content=content, photo_url=photo_url, starting_bid=starting_bid, category=category, date=datetime.datetime.now())
            newListing.save()
            firstBid = Bid(owner=user, value=starting_bid, listing=newListing, date=datetime.datetime.now())
            firstBid.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/createlisting.html", {
            "form": ListingForm()
        })
        
@login_required
def viewlisting(request, id):
    listing = Listing.objects.get(id=id)
    return render(request, "auctions/viewlisting.html", {
        "listing": listing,
        "bid": Bid.objects.get(listing=Listing.objects.get(id=id)),
        "form_comment": CommentForm(),
        "comments": listing.listing_comment.all().order_by('-date'),
        "watchlist": Watchlist.objects.filter(owner=request.user, listing=listing).exists()
    })
    
    
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.CATEGORIES
    })
    
def category(request, category):
    category_type = None
    for category_name in Category.CATEGORIES:
        if category_name[1] == category:
            category_type = category_name[0]
            break
    
    listings = Listing.objects.filter(category=Category.objects.get(category_type=category_type))
    return render(request, "auctions/category.html", {
        "listings": listings,
        "category": category
    })

def comment(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            content = form.cleaned_data['content']
            listing = Listing.objects.get(id=id)
            date = datetime.datetime.now()
            newComment = Comment(owner=user, content=content, listing=listing, date=date)
            newComment.save()
    return redirect('viewlisting', id=int(id))

def watchlist(request):
    return render(request, "auctions/watchlist.html")

def addtowatchlist(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        if not Watchlist.objects.filter(owner=request.user, listing=listing).exists():
            newWatchlist = Watchlist(owner=request.user, listing=listing)
            newWatchlist.save()
            print(Watchlist.objects.filter(owner=request.user, listing=listing))
        else:
            Watchlist.objects.filter(owner=request.user, listing=listing).delete()
            print(Watchlist.objects.filter(owner=request.user, listing=listing))

    return redirect('viewlisting', id=int(id))