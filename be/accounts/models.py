from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usernick = models.CharField(max_length=30, blank=True, null=True)
    profile_image = models.URLField(blank=True)

    def __str__(self):
        return self.usernick
