from django.db import models
from django.contrib.auth.models import User
from users.models import SBProfile


class Shop(models.Model):
    sid = models.CharField(max_length=8)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    teleph = models.CharField(max_length=11)

    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    remain = models.IntegerField(default=20)

    shop = models.ForeignKey(Shop)

    def __unicode__(self):
        return self.name


class Record(models.Model):
    rid = models.CharField(max_length=14)
    time = models.DateTimeField()
    status = models.IntegerField()
    money = models.FloatField()
    remark = models.CharField(max_length=1000)

    buyer = models.ForeignKey(User)
    shop = models.ForeignKey(Shop)
    sbpro = models.ForeignKey(SBProfile)

    def __unicode__(self):
        return self.rid


class Fooditem(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    quantity = models.IntegerField()

    record = models.ForeignKey(Record)

    def __unicode__(self):
        return self.name
