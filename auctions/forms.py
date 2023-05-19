from django.forms import ModelForm, Textarea

from .models import AuctionListing


# AuctionListing form
class AuctionListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["title", "description", "starting_bid", "category", "image_url"]
        widgets = {
            "description": Textarea()
        }
        
    def __init__(self, *args, **kwargs):
        super(AuctionListingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control form-control-sm my-2"