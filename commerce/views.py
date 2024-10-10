from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from auctions.models import Product, Category


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

        ## Create an object Category
        category = Category.objects.get(id=category_id)


        ## Create a Product object
        p = Product(name=title, category=category, description=description) #bid=bid
        p.save()

        return HttpResponse(f"<h1>Add NEW Enchères for: {p} Created!</h1>")
