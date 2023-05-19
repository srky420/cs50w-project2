from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


# Category choices
CATEGORIES = [
    ("CSA", "Clothing and Accessories"),
    ("SPT", "Sports"),
    ("HM", "Home"),
    ("ELT", "Electronics"),
    ("TY", "Toys"),
    ("BMD", "Books and Media"),
    ("HAB", "Health and Beauty"),
    ("OTH", "Others")
]


# User model
class User(AbstractUser):
    pass


# AuctionList model
class AuctionListing(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=100)
    starting_bid = models.IntegerField()
    category = models.CharField(max_length=64, choices=CATEGORIES)
    image_url = models.ImageField(upload_to="images/", null=True, blank=True)
    date_created = models.DateTimeField(default=datetime.datetime.now())
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")

    def __str__(self):
        return f"{self.title} by {self.owner} on {self.date_created}"
    
    
# Bid model
class Bid(models.Model):
    amount = models.IntegerField()
    date_created = models.DateTimeField(default=datetime.datetime.now())
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="biddings")
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    
    def __str__(self):
        return f"{self.bidder} placed a bid of: {self.amount} for {self.auction} on {self.date_created}"
    

# Comment model
class Comment(models.Model):
    text = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    date_created = models.DateTimeField(default=datetime.datetime.now())
    
    def __str__(self):
        return f"{self.owner} commented: \"{self.text}\" on {self.auction}"

