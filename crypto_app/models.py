from django.db import models
from django.contrib.auth.models import User


class Crypto(models.Model):
    symbol = models.CharField(max_length=20, unique=True)
    user = models.ManyToManyField(User, related_name="crypto_user", blank=True)
