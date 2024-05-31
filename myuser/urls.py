from django.contrib import admin
from django.urls import include, path

from myuser import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path ('logout/', views.logout, name='logout'),
    path('posts/', views.posts, name='posts'),
    path('profile/', views.profile, name='profile'),
    path('user/<str:username>/<int:pk>/', views.user_profile, name='user_profile'),
    path('follow/<str:username>/<int:pk>/', views.follow, name='follow'),
    path('share/<int:post_id>/', views.share_post, name='share_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('search/', views.search, name='search'),
]



