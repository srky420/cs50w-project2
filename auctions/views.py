from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, AuctionListing
from .forms import AuctionListingForm


def index(request):
    # Get all auction listings
    auctions = AuctionListing.objects.all()
    
    return render(request, "auctions/index.html", {
        "auctions": auctions
    })


def login_view(request):
    # POST
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username or password!")
            return render(request, "auctions/login.html")
    # GET
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    # POST
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Invalid username or password!")
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken!")
            return render(request, "auctions/register.html")
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    # GET
    else:
        return render(request, "auctions/register.html")


# Create listing
@login_required
def create_listing(request):
    # POST 
    if request.method == "POST":
        form = AuctionListingForm(request.POST, request.FILES)
        
        # Check form
        if form.is_valid():
            # Get form data
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            
            messages.success(request, "Auction Listing Created!")
            return HttpResponseRedirect(reverse("index"))
        # Invalid form
        else:
            messages.error(request, "Invalid form submission!")
            return render(request, "auctions/create-listing.html", {
                "form": form
            })
            
    # GET
    form = AuctionListingForm()
    return render(request, "auctions/create-listing.html", {
        "form": form
    })
    
    
# View listing
def view_listing(request, listing_id):
    # Get listing obj
    listing = AuctionListing.objects.get(pk=listing_id)
    
    # Get bids
    
    
    return render(request, "auctions/listing.html", {
        "listing": listing
    })
    

    