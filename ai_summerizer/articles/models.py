from django.db import models

# Create your models here.
class Article(models.Model):
    original_text = models.TextField()
    summary = models.TextField()
    tags=models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.summary[:50]
