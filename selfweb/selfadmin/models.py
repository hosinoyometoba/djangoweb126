from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=32)
    name = models.CharField(max_length=16,null=True)
    password = models.CharField(max_length=100)
    sex = models.IntegerField(null=True)
    address = models.CharField(max_length=255,null=True)
    code = models.CharField(max_length=6,null=True)
    phone = models.CharField(max_length=16,null=True)
    email = models.CharField(max_length=50)
    state = models.IntegerField(null=True,default=0)
    addtime = models.DateTimeField(auto_now_add=True)
    pic = models.CharField(max_length=100,null=True)

    
