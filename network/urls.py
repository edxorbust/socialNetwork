
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("user_profile/<int:id>", views.user_profile, name="user_profile"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("unfollow/<int:id>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("like_post/<int:post_id>", views.like_post, name="like_post"),
    path("unlike_post/<int:post_id>", views.unlike_post, name="unlike_post")
]
