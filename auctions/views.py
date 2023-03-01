from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import ListingForm, CommentForm
from .models import User, Listing, Category, Bid, Comment, Watchlist, Winner
import datetime


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True).order_by('-date'),
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
        return render(request, "auctions/login.html", {
            "message": "Invalid username and/or password."
        })
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
    return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            photo_url = form.cleaned_data['photo_url']
            starting_bid = form.cleaned_data['starting_bid']
            date = datetime.datetime.now()
            if form.cleaned_data['category']:
                category = Category.objects.get(category_type=form.cleaned_data['category'])
            else:
                category = Category.objects.get(category_type="NO")
            if not title or not content or not starting_bid:
                messages.error = "Please provide all the required information"
                return redirect('create_listing')
            newListing = Listing(owner=user, title=title, content=content, photo_url=photo_url, starting_bid=starting_bid, category=category, date=date)
            newListing.save()
            # Starting bid is the first bid on each listing
            firstBid = Bid(owner=user, value=starting_bid, listing=newListing, date=date)
            firstBid.save()

        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/createlisting.html", {
        "form": ListingForm()
    })
        
def view_listing(request, id):
    listing = Listing.objects.get(id=id)
    bids = Bid.objects.filter(listing=listing)
    bids_ordered_by_value = bids.order_by('-value')
    bid_counter = bids.count()
    comments_ordered_by_date = listing.listing_comment.all().order_by('-date')
    
    if Winner.objects.filter(listing=listing).exists():
        winner = Winner.objects.get(listing=listing).winner
    else:
        winner = None
    # Get rid of error that might appear due to changes in Django admin interface
    if bid_counter < 1:
        bid_counter = 1
    if request.user.is_authenticated:
        if bid_counter > 1:
            # ~Q excludes bid, which was the initial bid of listing owner
            # It allows to prompt "Your bid is the highest" to the user who placed a bid at the same value as the auction's creator
            highest_bid_owner = bids.filter(~Q(owner=listing.owner)).order_by('-value').first().owner
        else:
            highest_bid_owner = bids_ordered_by_value.first().owner
        return render(request, "auctions/viewlisting.html", {
            "listing": listing,
            "bid": bids_ordered_by_value,
            "bid_counter": bid_counter,
            "form_comment": CommentForm(),
            "comments": comments_ordered_by_date,
            "watchlist": Watchlist.objects.filter(owner=request.user, listing=listing).exists(),
            "winner": winner,
            "highest_bid_owner": highest_bid_owner
        })
    else:
        return render(request, "auctions/viewlisting.html", {
            "listing": listing,
            "bid": bids_ordered_by_value,
            "bid_counter": bid_counter,
            "form_comment": CommentForm(),
            "comments": comments_ordered_by_date,
            "winner": winner
        })

def user_listings(request, username):
    user = User.objects.get(username=username)
    return render(request, "auctions/userlistings.html", {
        "listings": Listing.objects.filter(owner=user).order_by('-date'),
        "bid": Bid.objects.order_by('value')
    })
    
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.CATEGORIES
    })
    
def category(request, category):
    category_type = ''
    for category_name in Category.CATEGORIES:
        if category_name[1] == category:
            category_type = category_name[0]
            break
    
    listings = Listing.objects.filter(category=Category.objects.get(category_type=category_type), active=True).order_by('-date')
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
    return redirect('view_listing', id=int(id))

def watchlist(request):
    watchlist = Watchlist.objects.filter(owner=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def add_or_remove_from_watchlist(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        user_watchlist = Watchlist.objects.filter(owner=request.user, listing=listing)
        # If no watchlist for logged user and specific listing exists, then create one
        if not user_watchlist.exists():
            newWatchlist = Watchlist(owner=request.user, listing=listing)
            newWatchlist.save()
        # If watchlist for logged user and specific listing exists, delete it
        else:
            user_watchlist.delete()
    # If button clicked on watchlist site, then redirect back to watchlist site
    # If button clicked on viewlisting site, then redirect back to watchlist site
    if request.POST.get("add_or_remove_from_watchlist") == "watchlist":
        return redirect('watchlist')
    else:
        return redirect('view_listing', id=int(id))
    
def place_bid(request, id):
    if request.method == "POST":
        bidvalue = float(request.POST.get("bidvalue"))
        listing = Listing.objects.get(id=id)
        bid = Bid.objects.filter(listing=listing)
        highestbid = float(bid.order_by('-value').first().value)
        bidcounter = bid.count()
        # bidcounter == 1 means that no one bid for the listing yet
        # The first bid is the auction creator's bid
        if bidcounter == 1:
            if bidvalue >= highestbid:
                newBid = Bid(owner=request.user, value=bidvalue, listing=listing, date=datetime.datetime.now())
                newBid.save()
            else:
                messages.error(request, 'Your bid must equal or higher than the current one.')
                return redirect('viewlisting', id=int(id))
        else:
            if bidvalue > highestbid:
                newBid = Bid(owner=request.user, value=bidvalue, listing=listing, date=datetime.datetime.now())
                newBid.save()
            else:
                messages.error(request, 'Your bid must be higher than the current one.')
                return redirect('view_listing', id=int(id))
    return redirect('view_listing', id=int(id))

def close_listing(request, id):
    # Closing the listing
    listing = Listing.objects.get(id=id)
    listing.active = False
    listing.save()
    # Saving winner
    highest_bid = Bid.objects.filter(listing=listing).order_by('-value').first()
    winner = Winner(winner=highest_bid.owner, listing=listing)
    winner.save()
    return redirect('view_listing', id=int(id))

def closed_listings(request):
    return render(request, "auctions/closedlistings.html", {
        "listings": Listing.objects.filter(active=False).order_by('-date'),
        "bid": Bid.objects.order_by('value')
    })

@login_required
def won_listings(request):
    # Excluding listings which were created by the logged user
    # The only listings won by the creator are the ones closed without any external bid
    # Such listings won't be shown as "won", but will be present in "My listings" tab
    
    # List of listing IDs which logged user is not an owner of
    listing_ids = Listing.objects.filter(~Q(owner=request.user)).values_list('id', flat=True).order_by('-date')
    # QuerySet of listings which were won by the logged user, but without these which were created by them
    won_listings = Winner.objects.filter(winner=request.user, listing__id__in=listing_ids)
    
    
    return render(request, "auctions/wonlistings.html", {
        "listings": won_listings
    })