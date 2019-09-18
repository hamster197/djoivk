from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class UserProfileVK(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    act = models.CharField(verbose_name='access_token', max_length=475, blank=False, null=False)