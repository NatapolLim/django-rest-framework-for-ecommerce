import os
from django.contrib.auth.models import User
from django.db import models

from django.utils.deconstruct import deconstructible

@deconstructible
class GenerateImagePath(object):
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/accounts/{instance.user.id}/image/'
        name = f'main.{ext}'
        return os.path.join(path, name)

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    image = models.FileField(upload_to=GenerateImagePath(), null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.user.id}|{self.user.username}'


# class Favourite(models.Model):
#     pass