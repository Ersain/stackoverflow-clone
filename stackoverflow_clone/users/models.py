from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(models.Model):
    reputation = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class User(AbstractUser):
    profile = models.OneToOneField(Profile, on_delete=models.DO_NOTHING)
    email = models.EmailField('email address', blank=True, unique=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        profile = Profile.objects.create()
        self.profile = profile
        super().save(*args, **kwargs)
