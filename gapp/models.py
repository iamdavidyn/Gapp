from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here

class CustomUser(AbstractUser):
    is_approved = models.BooleanField(default=False)
    session_key = models.CharField(max_length=50, blank=True, null=True)