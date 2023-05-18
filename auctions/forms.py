from django.forms import ModelForm

from .models import AuctionListing


# AuctionListing form
class AuctionListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["title", "description", "starting_bid", "category", "image_url"]
