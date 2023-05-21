from django.forms import ModelForm, Textarea, NumberInput

from .models import AuctionListing, Bid


# AuctionListing form
class AuctionListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["title", "description", "starting_bid", "category", "image"]
        widgets = {
            "description": Textarea()
        }
        
    def __init__(self, *args, **kwargs):
        super(AuctionListingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control form-control-sm mx-auto w-50 my-2 rounded-0 border-dark-subtle"

        
# Place bid form
class PlaceBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
        widgets = {
            "amount": NumberInput(attrs={"class": "form-control form-control-sm w-50 my-1 rounded-0 border-dark-subtle"})
        }
            
            
