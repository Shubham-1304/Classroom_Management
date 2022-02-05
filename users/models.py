from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200, blank=True,null=True)
    email=models.EmailField(max_length=500,blank=True,null=True)
    username=models.CharField(max_length=200, blank=True,null=True)

    def __str__(self) -> str:
        return str(self.user.username)
