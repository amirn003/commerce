from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    code = models.CharField(max_length=10)
    details = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.code}: {self.details}"


class Product(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_ref")
    description = models.TextField()
    initial_price = models.IntegerField(default=1)
    #picture = models.ImageField(upload_to='pictures/', blank=True, null=True, default='pictures/default.jpeg') #this is to store an image
    # picture as an URL
    picture = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.category}): {self.description}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bid_product_ref")
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.amount} ({self.time})"


class Comment(models.Model):
    title = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return f"{self.title}: {self.description}"


class AuctionListing(models.Model):
    # title = models.CharField(max_length=10, default="New Auction")
    # description = models.CharField(max_length=64, default="None")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="listing_product_ref", null=True, blank=True)
    bid = models.ForeignKey(Bid, on_delete=models.SET_NULL, related_name="bid_ref", null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, related_name="comment_ref", null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.bid}: {self.comment} ({self.date})"
