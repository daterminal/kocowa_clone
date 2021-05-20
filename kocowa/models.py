from django.db import models
from django.urls import reverse
from django.conf import settings
from photo.models import Photo
from photo.fields import ThumbnailImageField
from django.contrib.auth.models import User

class Recommend(models.Model):
    member_no = models.IntegerField(db_column='member_no', default=0)
    recom1 = models.CharField(db_column='recom1', max_length=50)
    recom2 = models.CharField(db_column='recom2', max_length=50)
    recom3 = models.CharField(db_column='recom3', max_length=50)
    recom4 = models.CharField(db_column='recom4', max_length=50)
    recom5 = models.CharField(db_column='recom5', max_length=50)
    recom6 = models.CharField(db_column='recom6', max_length=50)
    recom7 = models.CharField(db_column='recom7', max_length=50)
    recom8 = models.CharField(db_column='recom8', max_length=50)
    update_dt = models.DateTimeField(db_column='update_dt', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'recommend'




