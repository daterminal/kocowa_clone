from django.db import models
from django.conf import settings
# Create your models here.

class UserMembership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_membership', on_delete=models.CASCADE)
    join_dt = models.DateTimeField(db_column='join_dt', auto_now_add=True)
    period_day = models.IntegerField(db_column='period_day',default=0)

    def __str__(self):
       return self.user.username

class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, related_name='subscription', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    def __str__(self):
      return self.user_membership.user.username