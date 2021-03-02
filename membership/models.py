from django.db import models
from django.conf import settings
# Create your models here.
from userauth.models import CustomUser

class CustomUserMembership(models.Model):
    customuser_id = models.ForeignKey(CustomUser, related_name='user_membership', on_delete=models.CASCADE)
    join_dt = models.DateTimeField('JOIN DATE',auto_now_add=True)
    period_day = models.IntegerField('PERIOD DAY', default=0)

    def __str__(self):
       return self.user.username

class Subscription(models.Model):
    user_membership = models.ForeignKey(CustomUserMembership, related_name='subscription', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    def __str__(self):
      return self.user_membership.user.username
