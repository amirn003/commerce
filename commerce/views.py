from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from auctions.models import Product, Category, Bid, Comment, AuctionListing


# def index(request):
#     return HttpResponse("Commerce Index")

def create(request):
    categories = Category.objects.all()
    category_info = Category.objects.values('code')
    #categories = Category.objects.get(code="VEH")
    return render(request, "auctions/create.html", {
        "categories": categories,
        "category_info": category_info
    })


def add(request):
    if request.method == "POST":

        ## Retrive data from the Post request
        title = request.POST["title"]
        description = request.POST["description"]
        bid = int(request.POST["bid"])
        category_id = request.POST["category"]
        current_user = request.user
        #picture = request.FILES.get("picture") # to capture an image
        picture = request.POST["picture"]

        ## Create an object Category
        category = Category.objects.get(id=category_id)

        ## Create a Product object
        p = Product(user=current_user, name=title, category=category, description=description, initial_price=bid, picture=picture) #bid=bid
        p.save()

        ## Attach this Product object to a Bid object and set the price with the starting bid given in the form
        b = Bid(user=current_user, owner=True, product=p, amount=bid)
        b.save()

        # c = Comment(title=f"{title} Comment", description="details")
        # c.save()

        a = AuctionListing(product=p, bid=b)
        a.save()

        return HttpResponse(f"<h1>New Listing added with success by <i>{current_user}</i>.<br><a href='/{a.id}'>Go to this article</a></h1>")
