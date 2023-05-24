from django.forms import ModelForm, Textarea, NumberInput, TextInput, ImageField

from .models import AuctionListing, Bid, Comment


# AuctionListing form
class AuctionListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["title", "description", "starting_bid", "category", "image", "second_image", "third_image"]
        widgets = {
            "description": Textarea(),
        }
        labels = {
            "image": "Pictures (optional)",
            "second_image": "",
            "third_image": "",
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
            "amount": NumberInput(attrs={"class": "form-control form-control-sm w-50 my-1 rounded-0 border-dark-subtle",
                                         "placeholder": "$"})
        }


# Comment form
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {
            "text": ""
        }
        widgets = {
            "text": TextInput(attrs={"class": "form-control form-control-sm border-dark-subtle rounded-0 my-1 w-50",
                                     "placeholder": "Add a comment"})
        }
