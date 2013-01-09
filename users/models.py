from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class SBProfile(models.Model):
    user = models.OneToOneField(User)

    sbid = models.CharField(max_length=8)
    name = models.CharField(max_length=20)
    teleph = models.CharField(max_length=11)
    address = models.CharField(max_length=50)
    flag = models.IntegerField()

    def __unicode__(self):
        return self.name