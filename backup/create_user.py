from users.models import SBProfile
from random import randint


def insert_user():
    u, p = SBProfile.create_user('ysyong', 'ysyong', '1156546473@qq.com')
    u.is_staff = True
    u.is_superuser = True
    u.save()
    p.sbid = 20101472
    p.name = 'ysyong'
    p.teleph = '18990145486'
    p.address = 'D6A202'
    p.flag = 1
    print p, '111111111'
    p.save()

    for i in xrange(10):
        username = 'wimi' + str(i)
        email = username + '@qq.com'
        u, p = SBProfile.create_user(username=username,
            password=username, email=email)
        p.sbid = '8888888' + str(i)
        p.name = username
        p.teleph = '1899014548' + str(i)
        p.address = username
        p.flag = randint(0, 1)
        print p, '2222222222222'
        p.save()
