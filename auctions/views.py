from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, AuctionListing, Watchlist, Bid, Comment, Category, Winner
from .forms import AuctionListingForm, PlaceBidForm, CommentForm


def index(request):
    # Get all auction listings
    auctions = AuctionListing.objects.filter(is_closed=False).all()
    
    # Get all bids
    bids = []
    for auction in auctions:
        bids.append(auction.bids.all().order_by("-amount").first())
        

    zipped_list = zip(auctions, bids)
    
    return render(request, "auctions/index.html", {
        "zipped_list": zipped_list,
        "categories": Category.objects.all()
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
            messages.success(request, "Logged In.")
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
    
    # Get comments
    comments = listing.comments.all()
    
    # Check if listing closed
    if listing.is_closed:
        return render(request, "auctions/closed-listing.html", {
            "listing": listing,
            "bids": bids,
            "winner_bid": current_bid,
            "comments": comments
        })
    
    # Get watchlist obj
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user, auction=listing).first()
    else:
        watchlist = None
    
    # forms
    placebid_form = PlaceBidForm()
    comment_form = CommentForm()
    
    return render(request, "auctions/active-listing.html", {
        "listing": listing,
        "current_bid": current_bid,
        "bids": bids,
        "watchlist": watchlist,
        "placebid_form": placebid_form,
        "comment_form": comment_form,
        "comments": comments
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
        bid = auction.bids.all().order_by("-amount").first()
        
        # Save winner if any
        if bid:
            winner = Winner(user=bid.bidder, auction=auction)
            winner.save()
        
        auction.is_closed = True
        auction.save()
        
        return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))
            
       
# View watchlist
@login_required
def view_watchlist(request):
    # Get user's watchlist
    watchlist = Watchlist.objects.filter(user=request.user).all()
    
    # Create auctions list
    auctions = []
    for w in watchlist:
        auctions.append(w.auction)
    
    # Create bids list
    bids = []
    for auction in auctions:
        bids.append(auction.bids.all().order_by("-amount").first())
    
    # Zip both lists
    zipped_list = zip(auctions, bids)
    
    return render(request, "auctions/watchlist.html", {
        "zipped_list": zipped_list
    })
    

# Add comment
@login_required
def add_comment(request, listing_id):
    # POST
    if request.method == "POST":
        form = CommentForm(request.POST)
        
        if form.is_valid():
            text = form.cleaned_data["text"]
            auction = AuctionListing.objects.get(pk=listing_id)

            comment = Comment(text=text, owner=request.user, auction=auction)
            comment.save()
            
            messages.success(request, "Comment added.")
            return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))
        else:
            messages.error(request, "Error adding comment.")
            return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))
        

# Delete comment
@login_required
def delete_comment(request, listing_id):
    # POST
    if request.method == "POST":
        comment_id = request.POST["comment_id"]
        comment = Comment.objects.get(pk=comment_id)
        
        # Delete user's comment
        if comment.owner == request.user:
            comment.delete()
        
        return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))
    
    
# View your listings
@login_required
def your_listings(request):
    # Get all owned auctions
    auctions = AuctionListing.objects.filter(owner=request.user).all()
    bids = []
    for auction in auctions:
        bids.append(auction.bids.all().order_by("-amount").first())
        
    zipped_list = zip(auctions, bids)
    
    # Get all won listings
    winnings = Winner.objects.filter(user=request.user)
    
    auctions_won = []
    winning_bids = []
    
    for w in winnings:
        auctions_won.append(w.auction)
        winning_bids.append(w.auction.bids.all().order_by("-amount").first())

    zipped_list_winnings = zip(auctions_won, winning_bids)

    return render(request, "auctions/your-listings.html", {
        "zipped_list": zipped_list,
        "zipped_list_winnings": zipped_list_winnings
    })
    
    
# View categories
def view_categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })
    
    
# View category specific
def view_category(request, name):
    # Get category, auctions, bids
    category = Category.objects.get(name=name)
    auctions = AuctionListing.objects.filter(is_closed=False, category=category).all()
    bids = []
    for auction in auctions:
        bids.append(auction.bids.all().order_by("-amount").first)
        
    zipped_list = zip(auctions, bids)
    
    return render(request, "auctions/index.html", {
        "zipped_list": zipped_list,
        "categories": Category.objects.all(),
        "category": category
    })
    