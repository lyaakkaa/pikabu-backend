from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PeekabooUser(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    total_rating = models.IntegerField(default=0)
    role = models.CharField(max_length=50, default='user')

    def __str__(self) -> str:
            return self.username

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(PeekabooUser, on_delete=models.CASCADE, related_name='posts')
    created_date = models.DateTimeField(auto_now_add=True)
    body = models.TextField(default='')
    post_likes = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self) -> str:
        return self.title   


class Comment(models.Model):
    author = models.ForeignKey(PeekabooUser, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    comment_likes = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')


    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self) -> str:
        return f'{self.author}`s comment for {self.post}'




