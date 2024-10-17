from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListing, Watchlist


def index(request):
    active_listing = AuctionListing.objects.filter(active=True)

    return render(request, "auctions/index.html", {
        "active_listing": active_listing
    })

@login_required
def page(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    return render(request, "auctions/page.html", {
        "listing": listing
    })
    #return HttpResponse(f"<h1>Listing Page: {listing_id}</h1>")

@login_required
def add_to_watchlist(request, listing_id):
    current_user = request.user
    current_user_id = request.user.id
    listing = AuctionListing.objects.get(id=listing_id)
    watchlist = Watchlist.objects.filter(user=current_user_id, auction=listing)

    if listing.bid.user == current_user:
        return HttpResponse(f"<h1>This item: {listing.bid} is yours. You cannot add it to your watchlist.</h1>")

    elif watchlist:
        return HttpResponse(f"<h1>This item: {listing.bid} is already in your Watchlist.</h1>")

    else:
        watchlist = Watchlist(user=current_user, auction=listing, state=True)
        watchlist.save()
        return HttpResponse(f"<h1>Listing ID: {listing_id} added to {current_user}'s Watchlist ({request.user.id})!</h1>")


@login_required
def remove_from_watchlist(request, listing_id):
    current_user = request.user
    current_user_id = request.user.id
    listing = AuctionListing.objects.get(id=listing_id)
    watchlist = Watchlist.objects.filter(user=current_user_id, auction=listing)

    if watchlist.exists():
        watchlist.delete()
        return HttpResponse(f"<h1>Item: {listing.bid} removed from your <a href='/watchlist/'>Watchlist</a>.</h1>")

    else:

        return HttpResponse(f"<h1>Item: {listing_id} is not yet in your <a href='/watchlist/'>Watchlist</a>.</h1>")


@login_required
def watchlist(request):
    current_user_id = request.user.id
    watchlist = Watchlist.objects.filter(user=current_user_id)

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


@login_required
def bid(request):
    pass


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
