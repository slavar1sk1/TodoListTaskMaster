''' Create Model for Users'''

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create User model
class User(AbstractUser):
    pass

class UserProfile(models.Model):
    BRONZE = 'bronze'
    SILVER = 'silver'
    GOLD = 'gold'
    
    STATUS_CHOICES = [
        (BRONZE, 'Bronze'),
        (SILVER, 'Silver'),
        (GOLD, 'Gold'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=BRONZE)
    tasks_completed = models.IntegerField(default=0)


class TaskModel(models.Model):
    task = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tasks', default=1)
   
    