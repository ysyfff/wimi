#! /usr/bin/evn python
# -*-encoding:utf8-*-
from shops.models import Shop, Food
from django.contrib.auth.models import User
from random import randint


food = ['蘸水牛筋冻', '沾酱黄瓜', '柚子沙拉虾', '小米椒牛肉',
'香糟小黄鱼', '香糟毛豆', '香菜干丝', '乡村小木耳',
'土豆泥', '炭烧猪颈肉', '随便', '蒜泥拍黄瓜'
'酸奶芦荟鲜果', '四川泡菜', '手撕椒麻鸡', '上上签',
'三丝拌金针', '青椒小皮蛋', '皮蛋拌豆腐', '剁椒凤爪',
'糯米糖藕', '宁式烤菜', '乐山豆腐', '蜜汁小番茄',
'秘制拌面', '麻辣鹅胗', '麻酱油麦菜', '萝卜丝拌海蜇',
'韭菜鸡蛋干', '芥末黄喉', '椒香鸭掌', '泡菜凤爪',
'鸡丝荞面', '花椒鸭', '拌鸡尾菜', '红油猪耳',
'烤子鱼', '麻辣豆筋', '香椿拌白肉', '烧青椒拌海螺',
'爽口西芹', '贡菜肚丝', '橄榄菜拌龙豆', '干拌羊肚',
'干拌牛肉', '夫妻肺片', '拌西葫瓜', '川北凉粉',
'钵钵鸡', '冰镇萝卜', '冰镇蓝莓芦荟']
price = ['21', '9', '25', '25', '22', '9', '15',
    '15', '9', '9', '9', '21', '9', '25', '25',
    '15', '9', '9', '9', '21', '9', '25', '25',
    '15', '9', '9', '9', '21', '9', '25', '25',
    '15', '9', '9', '9', '21', '9', '25', '25',
    '15', '9', '9', '9', '21', '9', '25', '25',
    '22', '9', '15']

fp = zip(food, price) 


def insert_store():
    store_n = 1
    for i in xrange(1, 10):
        sid = '6666666' + str(i)
        teleph = '1355086238' + str(i)
        owner = User.objects.get(pk=i)
        p = owner.get_profile()
        name = p.name
        if p.flag == 0:
            s = Shop.objects.create(sid=sid, name=name, address=name,
                teleph=teleph, owner=owner)
            s.save()
            print 'create store success!'
            store_n = store_n + 1
        else:
            print 'this user is a buyer!'

    for i in xrange(1, store_n):
        s = Shop.objects.get(pk=i)
        for f in fp:
            food = Food.objects.create(name=f[0], price=f[1], shop=s)
            food.save()
            print('create food success!')
