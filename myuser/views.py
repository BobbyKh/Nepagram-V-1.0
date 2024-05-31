from pyexpat.errors import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login 
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q
from myuser.models import Follow, Like, Notification, Post, Profile
from myuser.models import Comment, Reply, Share





# Create your views here.
@login_required
def index(request):
    posts = Post.objects.all()
    posts = posts.annotate(like_count=Count('like'))
    share_posts = Share.objects.all()
    

    
    return render(request, 'pages/index.html', {'posts': posts , 'share_posts': share_posts} )



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
        except User.DoesNotExist:
            return render(request, 'pages/login.html', {'error': 'Invalid username or password. Please check your username and password'})
    return render(request, 'pages/login.html', {'error': 'Invalid username or password. Please check your username and password'})


def signup(request):
    
    if request.method == 'POST':
        # Handle form submission
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            return render(request, 'pages/signup.html', {'error': 'Passwords do not match. Please check your passwords'})
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except ValueError:
            return render(request, 'pages/signup.html', {'error': 'Invalid username or password. Please check your username and password'})
    
        return HttpResponseRedirect(reverse('login'))

    return render(request, 'pages/signup.html')
        




def logout(request):
    
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))

def posts(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        author = request.user
        post = Post.objects.create(title=title, content=content, author=author, image=image, video=video)
        return redirect('index')

    return render(request, 'pages/posts.html' )

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if user is not authenticated

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        image = request.FILES.get('image')
        bio = request.POST.get('bio')
        gender = request.POST.get('gender')
        cover = request.FILES.get('cover')

        if image:  # Update image only if it's provided
            profile.image = image
        if cover :
            profile.cover = cover
        if bio:  # Update bio only if it's provided
            profile.bio = bio
        if gender:  # Update gender only if it's provided
            profile.gender = gender
        
        profile.save()

    # Pass the profile object to the template
    return render(request, 'pages/profile.html', {'profile': profile})


@login_required
def user_profile(request, username, pk):
    user = get_object_or_404(User, username=username, pk=pk)
    posts = Post.objects.filter(author=user)
    profile = get_object_or_404(Profile, user=user)

    # Check if the authenticated user is already a follower of the profile user
    is_following = profile.user.followers.filter(id=request.user.id).exists()

    # Debugging statements
    print("Profile:", profile)
    print("Is following:", is_following.user)

    return render(request, 'pages/userprofile.html', {'user': user, 'posts': posts , 'profile': profile, 'is_following': is_following})

@login_required
def follow(request, username, pk):
    user_to_follow = get_object_or_404(User, username=username, pk=pk)

    # Check if the user is already following the target user
    is_following = Follow.objects.filter(follower=request.user, following=user_to_follow).exists()

    if is_following:
        # If already following, unfollow
        Follow.objects.filter(follower=request.user, following=user_to_follow).delete()
    else:
        # If not following, create a new follow relationship
        Follow.objects.create(follower=request.user, following=user_to_follow)

    # Redirect back to the user profile page
    return redirect('user_profile', username=username, pk=pk)@login_required
@login_required
def user_profile(request, username, pk):
    user = get_object_or_404(User, username=username, pk=pk)
    posts = Post.objects.filter(author=user)
    profile = get_object_or_404(Profile, user=user)


    # Check if the authenticated user is already a follower of the profile user
    is_following = Follow.objects.filter(follower=request.user, following=profile.user).exists()

    follower_count = Follow.objects.filter(following=profile.user).count()
    following_count = Follow.objects.filter(follower=profile.user).count()
    
    followers    = Follow.objects.filter(following=profile.user)
    following    = Follow.objects.filter(follower=profile.user)
    # Debugging statement
    print("Is following:", is_following)
    print("Follower count:", follower_count)
    print("Following count:", following_count)

    return render(request, 'pages/userprofile.html', {'user': user, 'posts': posts , 'profile': profile, 'is_following': is_following , 'follower_count': follower_count, 'following_count': following_count , 'followers': followers, 'following': following})

@login_required
def follow(request, username, pk):
    user_to_follow = get_object_or_404(User, username=username, pk=pk)

    # Check if the user is already following the target user
    follow_instance, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )

    if created:
        # If not following, create a new follow relationship
        notification_instance = Notification.objects.create(follow=follow_instance)

    else:
        # If already following, unfollow
        follow_instance.delete()

    # Redirect back to the user profile page
    return redirect('user_profile', username=username, pk=pk)

@login_required
def notification_page(request):
    # Get notifications for the current user
    notifications = Notification.objects.filter(author=request.user).order_by('-created_at')
    print(notifications)
    return render(request, 'layout.html', {'notifications': notifications})

def share_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    shared_user = post.author  # Assuming the author of the post is the user who shared it
    
    if request.method == 'POST':
        Share.objects.create(post=post, author=request.user)
        return redirect('index')  # Redirect to the posts page after sharing
    
    return render(request, 'pages/index.html', {'post': post, 'shared_user': shared_user})

def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    share_post = post.author
    if request.method == 'POST':
        like, created = Like.objects.get_or_create(post=post, author=request.user)
        if not created:
            like.delete()
        return redirect('index')  # Redirect to the posts page after liking or unliking
    
    
    return render(request, 'pages/index.html', {'post': post, 'share_post': share_post,})


def search(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', '').strip()
        if searched:
            # Using Q objects to allow case-insensitive and partial matching in the search
            users = User.objects.filter(Q(username__istartswith=searched) | Q(first_name__istartswith=searched) | Q(last_name__istartswith=searched))
            posts = Post.objects.filter(Q(title__istartswith=searched) | Q(content__istartswith=searched))
        else:
            users = User.objects.none()
            posts = Post.objects.none() 
            # Return an empty queryset if the search term is empty
        return render(request, 'pages/search.html', {'searched': searched, 'users': users, 'posts': posts})
    else:
        return render(request, 'pages/search.html', {})
    
