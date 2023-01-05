from django.db import models

# Create your models here.

class Board(models.Model):
    subject = models.CharField(max_length=250)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self) -> str:
        return self.subject

class Reply(models.Model):
    board = models.ForeignKey(Board,on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()