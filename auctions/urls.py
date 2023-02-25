from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("listing/<int:id>", views.viewlisting, name="viewlisting"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addtowachlist/<int:id>", views.addtowatchlist, name="addtowatchlist"),
    path("placebid/<int:id>", views.placebid, name="placebid"),
    path("closelisting/<int:id>", views.closelisting, name="closelisting"),
    path("closedlistings", views.closedlistings, name="closedlistings"),
    path("userlistings/<str:username>", views.userlistings, name="userlistings"),
    path("wonlistings", views.wonlistings, name="wonlistings")
]
