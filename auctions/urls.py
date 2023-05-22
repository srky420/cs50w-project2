from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing/", views.create_listing, name="create_listing"),
    path("<int:listing_id>/", views.view_listing, name="view_listing"),
    path("<int:listing_id>/watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("<int:listing_id>/close", views.close_listing, name="close_listing"),
    path("watchlist", views.view_watchlist, name="view_watchlist"),
    path("<int:listing_id>/comment", views.add_comment, name="add_comment"),
    path("<int:listing_id>/delete-comment", views.delete_comment, name="delete_comment"),
    path("your-listings/", views.your_listings, name="your_listings")
]
