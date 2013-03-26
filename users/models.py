#!usr/bin/evn python
#! -*- coding:utf8 -*-

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

    @classmethod
    def create_user(cls, username, password, email=None):
        user = User.objects.create_user(username=username,
            password=password, email=None)
        user.save()
        profile = cls.objects.get(user=user)
        return user, profile


def create_user_profile(sender, instance, created, **kwargs):
    """创建 userprofile 的方法.

    此为创建 User 时候的信号机制中创建 userprofile 的方法。
    signals 的细节请看官方文档:
           https://docs.djangoproject.com/en/1.4/topics/signals/
    """
    if created:
        SBProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
