from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    
    activation_key = models.CharField(max_length=40, blank=True, null=True)
    key_expires = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s"%(self.user.username)