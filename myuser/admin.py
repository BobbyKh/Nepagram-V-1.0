from django.contrib import admin

from myuser.models import  Comment, Follow, Like, Notification, Post, Profile, Reply, Share

# Register your models here.

post_models = [
  
    Post,
    Comment,
    Reply,
    Like,
    Share,
    Profile,
    Follow,
    Notification,
]
admin.site.register(post_models)
