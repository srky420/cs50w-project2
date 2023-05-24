from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


# User model
class User(AbstractUser):
    pass


# Category model
class Category(models.Model):
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return self.name


# AuctionList model
class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    starting_bid = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="auctions")
    image = models.ImageField(upload_to="images/", default="images/default.jpg")
    second_image = models.ImageField(upload_to="images/", default="images/default.jpg")
    third_image = models.ImageField(upload_to="images/", default="images/default.jpg")
    date_created = models.DateTimeField(default=datetime.datetime.now())
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.owner} on {self.date_created}"
    
    
# Bid model
class Bid(models.Model):
    amount = models.IntegerField()
    date_created = models.DateTimeField(default=datetime.datetime.now())
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="biddings")
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    
    def __str__(self):
        return f"{self.bidder} placed a bid of: {self.amount} for auction: {self.auction.title} on {self.date_created}"
    

# Comment model
class Comment(models.Model):
    text = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    date_created = models.DateTimeField(default=datetime.datetime.now())
    
    def __str__(self):
        return f"{self.owner} commented: \"{self.text}\" on auction: {self.auction.title}"
    

# Watchlist model
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlisted_by") 

    def __str__(self):
        return f"{self.user} watchlisted auction: {self.auction.title}"
    
    
# Winners model
class Winner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winnings")
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="winner")
    
    def __str__(self):
        return f"{self.user} won auction: {self.auction}"