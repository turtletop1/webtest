from django.db import models
from django.contrib.auth.models import User 
from posts.models import Post

class Comment (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content=models.TextField(blank=True)
    date = models.DateTimeField()

    def __str__(self):
        post_user_c = self.post.title + "_" + self.user.username
        return post_user_c