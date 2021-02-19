from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

SEX = (('MAN', 'Man'), ('WOMAN', 'Woman'))
# Create your models here.
class CustomUser(AbstractUser):
    age = models.IntegerField(verbose_name=_("Age"), blank=True, null=True)
    sexType = models.CharField(verbose_name=_("Sex"), max_length=9,choices=SEX, default="MAN")
    city = models.CharField(verbose_name=_("City"), max_length=1024, blank=True, null=True)

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"