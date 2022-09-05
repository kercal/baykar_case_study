from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    first_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    blocked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="blocked_by")
    #EMAIL_FIELD = 'email'
    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username
