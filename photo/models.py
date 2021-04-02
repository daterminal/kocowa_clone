from django.db import models
from django.urls import reverse
from django.conf import settings

from photo.fields import ThumbnailImageField
from django.contrib.auth.models import User

class Album(models.Model):
    name = models.CharField('NAME', max_length=30)
    description = models.CharField('One Line Description', max_length=100, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('photo:album_detail', args=(self.id,))


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField('TITLE', max_length=30)
    description = models.TextField('Photo Description', blank=True)
    image = ThumbnailImageField('IMAGE', upload_to='photo/%Y/%m')
    video_key = models.CharField('VIDEO KEY', max_length=30, null=True)
    upload_dt = models.DateTimeField('UPLOAD DATE', auto_now_add=True)
    love = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='loves', blank=True)
    photo_video_time = models.TimeField('PHOTO VIDEO TIME', null=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('photo:photo_detail', args=(self.id,))

