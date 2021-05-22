from django.db import models
from authentication.models import User


class Post(models.Model):
    """model for a post"""

    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(max_length=700, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"${self.title}"
