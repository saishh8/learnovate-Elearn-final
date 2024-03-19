from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_instructor = models.BooleanField(default=False, null=True)
    is_learner = models.BooleanField(default=False, null=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    



    
class Instructor(models.Model):
    email = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    linked_in_url = models.URLField(max_length=200, blank=False, null=False)
    resume = models.FileField(upload_to='resumes/', blank=False, null=False)
    is_validated = models.BooleanField(default=False, null=True)


    def __str__(self):
        return self.email.email
    

    def get_full_name(self):
        return f'{self.email.first_name} {self.user.last_name}'
    
    def get_short_name(self):
        return self.email.first_name
