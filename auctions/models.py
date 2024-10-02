from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction(models.Model):
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=32)
    price = models.IntegerField()
    description = models.TextField()
    date = models.DateField(auto_created=True)


class Bid(models.Model):
    pass


class Comment(models.Model):
    pass
