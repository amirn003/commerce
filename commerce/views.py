from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

def create(request):
    return HttpResponse("<h1> Create Your Enchère </h1>")
