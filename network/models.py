from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='user_followers')
    follows = models.ManyToManyField('self', symmetrical=False, related_name='user_follows')

class Post(models.Model):
    content = models.CharField(max_length=140)
    user = models.ForeignKey(User, related_name=("author"), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    likedBy = models.ManyToManyField(User, null=True, blank=True, related_name="likedBy")
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Post {self.id} by {self.user} on {self.date.strftime('%d %m %Y %H:%M:%S')}"
    
class Like(models.Model):
    postLiked = models.ForeignKey(Post, related_name=("postLiked"), on_delete=models.CASCADE)
    whoLiked = models.ForeignKey(User, null=True, related_name=("whoLiked"), on_delete=models.CASCADE)