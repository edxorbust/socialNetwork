from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
import json


from .models import User, Post, Like

def following(request):
    actualUser = request.user
    actualProfile = User.objects.get(pk=actualUser.id)
    whoFollows = actualProfile.follows.all()
    posts = Post.objects.filter(user__in=whoFollows).order_by('-date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user_in = request.user
    if user_in.is_authenticated:
        liked_post_ids = Like.objects.filter(whoLiked=user_in).values_list('postLiked_id', flat=True)
    else:
        liked_post_ids =[]
    return render(request, 'network/following.html', {
        'page_obj': page_obj,
        "userIn": user_in,
        "likedPostsId": liked_post_ids
        })


def follow(request, id):
    if request.method == "POST":
        actualUser = request.user
        profile = User.objects.get(pk=id)
        profile.followers.add(actualUser)
        actualProfile = User.objects.get(pk=actualUser.id)
        actualProfile.follows.add(profile)
        return HttpResponseRedirect(reverse("user_profile", args=(id,)))

def unfollow(request, id):
    if request.method == "POST":
        actualUser = request.user
        profile = User.objects.get(pk=id)
        profile.followers.remove(actualUser)
        actualProfile = User.objects.get(pk=actualUser.id)
        actualProfile.follows.remove(profile)
        return HttpResponseRedirect(reverse("user_profile", args=(id,)))


def user_profile(request, id):
    profile = User.objects.get(pk=id)
    postData = Post.objects.filter(user=profile).order_by('-date')
    followers = profile.followers.all().count()
    follows = profile.follows.all().count()
    paginator = Paginator(postData, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    userIn = request.user
    if userIn == profile:
        isAuthor = True
    else:
        isAuthor = False
    if userIn in profile.followers.all():
        alreadyFollow = True
    else:
        alreadyFollow = False

    if userIn.is_authenticated:
        liked_post_ids = Like.objects.filter(whoLiked=userIn).values_list('postLiked_id', flat=True)
    else:
        liked_post_ids =[]

    return render(request, "network/user_profile.html", {
        "posts":page_obj,
        "userProf":profile,
        "userIn": userIn,
        "followers":followers,
        "follows":follows,
        "alreadyFollow":alreadyFollow,
        "isAuthor":isAuthor,
        "profile":profile,
        "likedPostsId": liked_post_ids
    })


def edit_post(request):
    if request.method == "POST":
        #creating the variables
        content = request.POST["npost"]
        user = request.user

        editedPost = Post.objects.get(pk=request.POST["id-post"])
        if user == editedPost.user:
            editedPost.content = content
            editedPost.save()
        else:
            print("Invalid edition")

        return redirect(request.META.get('HTTP_REFERER'))



def new_post(request):
    if request.method == "POST":
        #creating the variables
        content = request.POST["npost"]
        user = request.user

        #creating the post
        nPost = Post(
            content = content,
            user = user
        )
        nPost.save()
        return HttpResponseRedirect(reverse("index"))


def index(request):
    postList = Post.objects.all().order_by('-date')
    paginator = Paginator(postList, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user_in = request.user
    if user_in.is_authenticated:
        liked_post_ids = Like.objects.filter(whoLiked=user_in).values_list('postLiked_id', flat=True)
    else:
        liked_post_ids =[]

    return render(request, "network/index.html", {
        "posts": page_obj,
        "userIn": user_in,
        "likedPostsId": liked_post_ids
    })


def login_view(request):
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")




def like_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("liked") is not None:
            post.likes = post.likes + 1
            actualUser = request.user
            post.likedBy.add(actualUser)
            newLike = Like(
                postLiked = post,
                whoLiked = actualUser
            )
            newLike.save()
            post.save()

        likes_count = post.likes

        response_data = {
            "likes": likes_count
        }
        print(response_data)
        return JsonResponse(response_data)


def unlike_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("liked") is not None:
            post.likes = post.likes - 1
            actualUser = request.user
            post.likedBy.remove(actualUser)
            likeToRemove = Like.objects.get(postLiked=post, whoLiked=actualUser )
            likeToRemove.delete()
            post.save()

        likes_count = post.likes

        response_data = {
            "likes": likes_count
        }
        print(response_data)
        return JsonResponse(response_data)