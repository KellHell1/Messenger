from django.db import models
from django.contrib.auth.models import User


class ImageProfile(models.Model):
    owner = models.ForeignKey(User, related_name='image', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="images/profile/")

