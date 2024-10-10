from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# def index(request):
#     return HttpResponse("Commerce Index")

def create(request):
    return render(request, "auctions/create.html")


def add(request):
    if request.method == "POST":

        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]

        return HttpResponse(f"<h1>Add NEW Enchères for: {title} - {description} -{bid} </h1>")
