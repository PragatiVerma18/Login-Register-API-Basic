from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_user = models.BooleanField(default=True, null=True)
    is_org = models.BooleanField(default=False,null=True)

    def __str__(self):
        return self.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
