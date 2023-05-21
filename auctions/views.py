from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, AuctionListing, Watchlist, Bid
from .forms import AuctionListingForm, PlaceBidForm


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
            messages.error(request, "Invalid username or password.")
            return render(request, "auctions/login.html")
    # GET
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out.")
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
            messages.error(request, "Invalid username or password.")
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, "auctions/register.html")
        
        login(request, user)
        messages.success(request, "Account created.")
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
            
            messages.success(request, "Auction Listing Created.")
            return HttpResponseRedirect(reverse("index"))
        # Invalid form
        else:
            messages.error(request, "Invalid form submission.")
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
    bids = listing.bids.all()
    
    # Check if auction has bids
    current_bid = bids.order_by("-amount").first()
    
    # Check if listing closed
    if listing.is_closed:
        return render(request, "auctions/closed-listing.html", {
            "listing": listing,
            "bids": bids,
            "winner_bid": current_bid
        })
    
    # Get watchlist obj
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user, auction=listing).first()
    else:
        watchlist = None
    
    # Place bid form
    form = PlaceBidForm()
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_bid": current_bid,
        "bids": bids,
        "watchlist": watchlist,
        "form": form
    })
        
        
# Add to watchlist
@login_required
def watchlist(request, listing_id):
    # Check if already watchlisted
    auction = AuctionListing.objects.get(pk=listing_id)
    watchlist = Watchlist.objects.filter(user=request.user, auction=auction).first()
    
    # Delete existing obj
    if watchlist:
        watchlist.delete()
        messages.error(request, "Removed from watchlist.")
    # Create new obj
    else:
        watchlist = Watchlist(user=request.user, auction=auction)
        watchlist.save()
        messages.success(request, "Added to watchlist.")
    
    return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))


# Place bid
@login_required   
def bid(request, listing_id):
    # POST
    if request.method == "POST":
        form = PlaceBidForm(request.POST)
        
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            
            # Checks
            auction = AuctionListing.objects.get(pk=listing_id)
            current_bid = auction.bids.all().order_by("-amount").first()
            
            # Check if bid exists
            if current_bid:
                if current_bid.bidder == request.user:
                    messages.error(request, "Your bid is the current bid.")
                    return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))
                
                current_bid = current_bid.amount
            else:
                current_bid = auction.starting_bid
            
            # If this bid less than current bid
            if amount <= current_bid:
                messages.error(request, "Invalid bid amount.")
                return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))
            
            bid = Bid(amount=amount, bidder=request.user, auction=auction)
            bid.save()
            
            messages.success(request, "Bid placed.")
            return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))
        else:
            messages.error(request, "Error placing bid.")
            return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))
        

# Close listing
@login_required
def close_listing(request, listing_id):
    # POST
    if request.method == "POST":
        auction = AuctionListing.objects.get(pk=listing_id)
        auction.is_closed = True
        auction.save()
        
        return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))
            
       
# View watchlist
@login_required
def view_watchlist(request):
    # Get user's watchlist
    watchlist = Watchlist.objects.filter(user=request.user).all()
    
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })