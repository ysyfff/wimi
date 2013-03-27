#! /usr/bin/evn python
# -*-coding:utf-8-*-
from django.contrib.auth.models import User
from users.models import SBProfile
from random import randint


def insert_user():
    u = User.objects.create_user(username='ysyong', email='1156546473@qq.com',
        password='ysyong')
    u.is_staff = True
    u.is_superuser = True
    u.save()
    sbid = '20101472'
    name = 'ysyong'
    teleph = '18990145486'
    address = 'D6A202'
    flag = 1 #buyer
    p = SBProfile.objects.create(sbid=sbid, name=name, teleph=teleph,
        address=address, flag=flag, user=u)
    p.save()
    print 'super user success!'

    for i in xrange(10):
        username = 'wimi' + str(i)
        email = username + '@qq.com'
        u = User.objects.create_user(username=username, email= email,
            password= username)
        u.save()
        sbid = '8888888' + str(i)
        name = username
        teleph = '1899014548' + str(i)
        address = username
        flag = randint(0, 1)
        p = SBProfile.objects.create(sbid=sbid, name=name, teleph=teleph,
            address=address, flag=flag, user=u)
        p.save()
        print 'other user success!'
