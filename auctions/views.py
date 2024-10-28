from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListing, Watchlist, Bid, Comment, Category, Product


def index(request):
    active_listing = AuctionListing.objects.filter(active=True)

    return render(request, "auctions/index.html", {
        "active_listing": active_listing
    })


def winning_strategy(won_listing, current_user_id):

    bid_win = []
    for won in won_listing:
        bid_id = won.bid.id
        bid = Bid.objects.filter(id=bid_id, user=current_user_id)
        if bid:
            bid_win.append(bid)

    return bid_win


def won(request):
    current_user_id = request.user.id
    current_user_obj = User.objects.get(id=current_user_id)
    won_listing = AuctionListing.objects.filter(active=False).exclude(product__user=current_user_obj)

    bid_win = winning_strategy(won_listing, current_user_id)

    if won_listing and len(bid_win) != 0:
        return render(request, "auctions/won.html", {
            "won_listing": won_listing
        })

    else:
        return render(request, "auctions/tryagain.html")


@login_required
def page(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    current_user_id = request.user.id
    won_listing = AuctionListing.objects.filter(active=False)
    active_listings = AuctionListing.objects.filter(active=True, id=listing_id)
    bid_win = winning_strategy(won_listing, current_user_id)
    you_win = False
    if len(bid_win) != 0:
        you_win = True

    return render(request, "auctions/page.html", {
        "listing": listing,
        "you_win": you_win,
        "active_listings": active_listings
    })
    #return HttpResponse(f"<h1>Listing Page: {listing_id}</h1>")

@login_required
def add_to_watchlist(request, listing_id):
    current_user = request.user
    current_user_id = request.user.id
    listing = AuctionListing.objects.get(id=listing_id)
    watchlist = Watchlist.objects.filter(user=current_user_id, auction=listing)

    # if listing.bid.user == current_user:
    #     return HttpResponse(f"<h1>This item: {listing.bid} is yours. You cannot add it to your watchlist.</h1>")
    if watchlist:
        return HttpResponse(f"<h1>This item: {listing.bid} is already in your Watchlist.</h1>")

    else:
        watchlist = Watchlist(user=current_user, auction=listing, state=True)
        watchlist.save()
        return HttpResponseRedirect(reverse("watchlist"))
        #return HttpResponse(f"<h1>Listing ID: {listing_id} added to {current_user}'s Watchlist ({request.user.id})!</h1>")


@login_required
def remove_from_watchlist(request, listing_id):
    current_user = request.user
    current_user_id = request.user.id
    listing = AuctionListing.objects.get(id=listing_id)
    watchlist = Watchlist.objects.filter(user=current_user_id, auction=listing)

    if watchlist.exists():
        watchlist.delete()
        return HttpResponseRedirect(reverse("watchlist"))

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
def bid(request, listing_id):
    if request.method == "POST":
        bid_user = request.POST["bid_user"]
        listing = AuctionListing.objects.get(id=listing_id)
        current_user_id = request.user.id
        current_user = request.user

        if listing.product.user.id == current_user_id:
            return HttpResponse(f"<h1>It's your product {current_user}. You cannot bid on it!</h1>")

        ##TODO: Check if the bid proposed is upper to the previous
        ## and set in the Bid object 'owner' to 'False'
        ## add the new bid with the user object
        if int(bid_user) > listing.bid.amount:
            current_user_obj = User.objects.get(id=current_user_id)
            my_bid = listing.bid.id
            current_bid_obj = Bid.objects.get(id=my_bid)
            current_bid_obj.owner = False
            current_bid_obj.user = current_user_obj
            current_bid_obj.amount = int(bid_user)
            current_bid_obj.save()
            return redirect(f'/{listing.id}')
            #return HttpResponse(f"<h1>{current_user}  tip {bid_user} $ - {listing.product.user} - {listing.bid} - {current_bid_obj}</h1>")
        else:
            return HttpResponse(f"<h1>Hi {current_user}! Please tip a bid over {listing.bid.amount}$.</h1>")


@login_required
def close(request, listing_id):
    if request.method == "POST":
        auction_state = request.POST.get('auction_state')
        listing = AuctionListing.objects.get(id=listing_id)
        if auction_state:
            listing.active = False
            listing.save()
            return HttpResponse(f"<h1> Bid Won by {listing.bid.user}!</h1>")

        else:
            return HttpResponse(f"<h1>Your item {listing} is still on bid.</h1>")


@login_required
def comment(request, listing_id):
    current_user_id = request.user.id
    current_user = request.user

    if request.method == "POST":
        current_user_obj = User.objects.get(id=current_user_id)
        title = request.POST["title"]
        description = request.POST["description"]
        listing = AuctionListing.objects.get(id=listing_id)

        comment = Comment(user=current_user_obj, title=title, description=description)
        comment.save()
        listing.comment.add(comment)

        return HttpResponse(f"<h1>Comment by {current_user} on {listing_id} - {title} - {description}</h1>")


def categories(request):
    categories = Category.objects.all()
    # category = Category.objects.get(id=2)
    # products_in_category = Product.objects.filter(category=category)
    # auction21 = AuctionListing.objects.filter(product__name="Harley Davidson")


    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def display_category(request, category_id):
    category_name = Category.objects.get(id=category_id).details

    products_filtered = Product.objects.filter(category=category_id)
    auctions_filtered_list = []

    if products_filtered:
        for product in products_filtered:
            auctions_filtered = AuctionListing.objects.filter(product__id=product.id)
            auctions_filtered_list.append(auctions_filtered)

    return render(request, "auctions/display_category.html", {
        "category_name": category_name,
        "category_id": category_id,
        "auctions_filtered_list": auctions_filtered_list
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
