from django.db import models

# Create your models here.

class Mountain(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    address = models.TextField()
    latitude = models.CharField(max_length=50) # 위도
    longitude = models.CharField(max_length=50) # 경도
    info = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Mountain_img(models.Model):
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE)
    img_url = models.CharField(max_length=50)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.mountain