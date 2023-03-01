from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="create_listing"),
    path("listing/<int:id>", views.view_listing, name="view_listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addtowachlist/<int:id>", views.add_or_remove_from_watchlist, name="add_or_remove_from_watchlist"),
    path("placebid/<int:id>", views.place_bid, name="place_bid"),
    path("closelisting/<int:id>", views.close_listing, name="close_listing"),
    path("closedlistings", views.closed_listings, name="closed_listings"),
    path("userlistings/<str:username>", views.user_listings, name="user_listings"),
    path("wonlistings", views.won_listings, name="won_listings")
]
