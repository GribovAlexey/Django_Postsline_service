from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title + " | " + str(self.author)

    class Meta:
        permissions = [
            ("view_private_posts", "Can view private posts"),
        ]
