from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Board(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_board')
    subject = models.CharField(max_length=250)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_board') # 추천인 추가

    def __str__(self) -> str:
        return self.subject

class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_reply')
    board = models.ForeignKey(Board,on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_reply')