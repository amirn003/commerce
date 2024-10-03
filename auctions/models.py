from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction(models.Model):
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=32)
    initial_price = models.IntegerField()
    description = models.TextField()
    date = models.DateField(auto_created=True)

    def __str__(self):
        return f"{self.name}: {self.description}"


class Bid(models.Model):
    user = models.CharField(max_length=64)
    offer = models.IntegerField()

    def __str__(self):
        return f"{self.user}: {self.offer}"


class Comment(models.Model):
