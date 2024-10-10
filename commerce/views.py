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
        categories: "categories",
        category_info: "category_info"
    })


def add(request):
    if request.method == "POST":

        ## Retrive data from the Post request
        title = request.POST["title"]
        description = request.POST["description"]
        bid = int(request.POST["bid"])


        ## Create the Product object
        p = Product(name=title, description=description) #bid=bid

        return HttpResponse(f"<h1>Add NEW Enchères for: {title} - {description} -{bid}</h1>")
