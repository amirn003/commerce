from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>", views.page, name="page"),
    path("<int:listing_id>/add", views.add_to_watchlist, name="add_to_watchlist"),
    path("<int:listing_id>/remove", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("<int:listing_id>/bid/", views.bid, name="bid"),
    path("<int:listing_id>/close/", views.close, name="close"),
    path("won/", views.won, name="won"),
    path("comment/", views.comment, name="comment"),
]
