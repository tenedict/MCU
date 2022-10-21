from django.db import models

# Create your models here.
class Review(models.Model):
    user = models.CharField(max_length=30)
    title = models.TextField()
    content = models.CharField(max_length=30)
    movie_name = models.CharField(max_length=30)
    grade = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)