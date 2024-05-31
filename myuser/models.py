from django.db import models
from django.contrib.auth.models import User

# Create your models here.


    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    cover = models.ImageField(default='default.jpg', upload_to='cover_pics')
    bio = models.TextField()
    gender = models.CharField(max_length=100)
    following = models.ManyToManyField(User, related_name='followers', blank=True)
    def is_following(self, user):
        return Follow.objects.filter(follower=self.user, following=user).exists()
    def __str__(self) -> str:
        return self.user.username      
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='post_pics', null=True, blank=True)
    video = models.FileField(upload_to='post_videos', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.comment    
    
class Reply(models.Model):
    reply = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.reply

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    
    def __str__(self) -> str:
        return f"{self.follower} follows {self.following}"
        
    
class Share(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shared_post')
    
    def __str__(self) -> str:
        return f"{self.shared_post} shared by {self.author} on {self.post}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.post} liked by {self.author}"

class Notification(models.Model):

    follow = models.ForeignKey(Follow, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification for {self.follow}"
    