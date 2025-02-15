from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from core.settings import AUTH_USER_MODEL


from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    token = models.CharField(max_length=50,blank=True,null=True)
    # ROLES_LIST = {
    #     "ADMIN" : "admin",
    #     "USER"  : "user"
    # }
    # role = models.CharField(max_length=10, choices=ROLES_LIST, default=ROLES_LIST["USER"])
    class Roles(models.TextChoices):
        ADMIN = 1
        USER = 2
    role = models.IntegerField(choices=Roles.choices, default=Roles.USER)
    
class Post(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField( max_length=50)
    content = models.TextField(blank=True,max_length=50000)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    likes = models.ManyToManyField(User, related_name="user_post")
    saved = models.ManyToManyField(User, related_name="user_save_post")
    verified = models.BooleanField(default=False)

            
class Comment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)   
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 