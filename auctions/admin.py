from django.contrib import admin

from .models import User, AuctionListing, Bid, Comment

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "password")


class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "starting_bid", "category", "image", "date_created", "owner")


class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "amount", "date_created", "bidder", "auction")
    

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "owner", "auction", "date_created")


admin.site.register(User, UserAdmin)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)