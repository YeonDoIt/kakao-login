from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usernick = models.CharField(max_length=100)
    profile_image = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birthday = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username
