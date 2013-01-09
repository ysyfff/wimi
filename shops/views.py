from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import datetime
import time
from django.utils import timezone

from users.models import SBProfile
from shops.models import Shop, Food, Record, Fooditem
from shops.forms import AddFoodForm

def shops(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        username = request.user.username
        is_login=True
        profile = SBProfile.objects.get(user_id=user_id)
        if profile.flag == 1:
            is_buyer = True
        else:
            is_buyer = False
    shop = Shop.objects.all()
    return render_to_response('shops/shop.html',
        locals(),
        context_instance=RequestContext(request)
    )

#get the shop's food info
#use one to visit many
def myshop(request, shop_id):
    errors_msg= []
    shop = get_object_or_404(Shop, pk=shop_id)
    if request.method=="POST":
        if request.user.is_authenticated():
            user_id = request.user.id
            username = request.user.username
            is_login=True
            profile = SBProfile.objects.get(user_id=user_id)
            if profile.flag == 1:
                is_buyer = True
            else:
                is_buyer = False
            selected_choose = request.REQUEST.getlist('choose')#######
            selected_quantity = request.REQUEST.getlist('quantity')
            remark = request.POST['remark']
            if not selected_choose:
                errors_msg.append('you do not choose anything!')
                return render_to_response('shops/myshop.html',
                    locals(),
                    context_instance=RequestContext(request)
                )
            else:
                money = 0;
                #create records
                length = len(selected_choose)
                for i in range(0,length):
                    sc = selected_choose[i]
                    qty = selected_quantity[i]
                    food = shop.food_set.get(pk=sc)
                    money = money + food.price*int(qty)
                print money
                rid = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
                nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                status = 1
                sbpro = request.user.get_profile()
                record = Record(rid=rid, time=nowtime, status=status, remark=remark, money=money, buyer=request.user, shop=shop, sbpro=sbpro)
                record.save()
                #create fooditem
                length = len(selected_choose)
                for i in range(0,length):
                    sc = selected_choose[i]
                    qty = selected_quantity[i]
                    food = shop.food_set.get(pk=sc)
                    fooditem = Fooditem(name=food.name, price=food.price, quantity=qty, record=record)
                    fooditem.save()
                Bag_PATH = '/shops/'+str(user_id)+'/current/bag/'
                return redirect(Bag_PATH)
        else:
            errors_msg.append('You have not logged in, so you can not buy anything!')
            return render_to_response('home.html',
                locals(),
                context_instance=RequestContext(request)
            )
    else:
        if request.user.is_authenticated():
            user_id = request.user.id
            username = request.user.username
            is_login=True
            profile = SBProfile.objects.get(user_id=user_id)
            if profile.flag == 1:
                is_buyer = True
            else:
                is_buyer = False
        return render_to_response('shops/myshop.html',
            locals(),
            context_instance=RequestContext(request)
        )

def badbag(request):
    errors_msg=[]
    errors_msg.append('You have not logged, so you can not see any bags!')
    return render_to_response('home.html',
        locals(),
        RequestContext(request)
    )

def curbag(request, user_id):
    if request.user.is_authenticated():
        user_id = request.user.id
        username = request.user.username
        is_login=True
        profile = SBProfile.objects.get(user_id=user_id)
        if profile.flag == 1:
            is_buyer = True
        else:
            is_buyer = False
        if is_buyer:    #####for buyer
            all_list = Record.objects.filter(buyer=request.user, status__exact=1).order_by('-time')
            count1 = all_list.count()
            all_list2 = Record.objects.filter(buyer=request.user, status__exact=4).order_by('-time')
            count2 = all_list2.count()
            all_list3 = Record.objects.filter(buyer=request.user, status__exact=2).order_by('-time')
            count3 = all_list3.count()
            all_list4 = Record.objects.filter(buyer=request.user, status__exact=3).order_by('-time')
            count4 = all_list4.count()
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            all_list5 = Record.objects.filter(buyer=request.user, rid__startswith=today).order_by('-time')
            count5 = all_list5.count()
            btoday = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            all_list6 = Record.objects.filter(buyer=request.user, time__lte=btoday).order_by('-time')
            count6 = all_list6.count()
            if request.method=="POST":
                #oper
                value = request.POST['oper']
                leng = len(value)
                ID = 0
                for i in range(1, leng):
                    ID = ID*10+int(value[i])
                r = Record.objects.get(pk=ID)
                if value[0]=='d':
                    r.status = 3
                    r.save()
                elif value[0]=='l':
                    r.status=2
                    r.save()
                Bag_PATH = '/shops/'+str(user_id)+'/current/bag/'
                return redirect(Bag_PATH)
            return render_to_response('shops/curbag.html',
                locals(),
                context_instance=RequestContext(request)
            )
        else:       ##### for seller
            user = request.user
            shop = user.shop_set.all()[:1]
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            btoday = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            for s in shop:
                all_list = Record.objects.filter(shop=s, status__exact=1).order_by('-time')
                count1 = all_list.count()
                all_list2 = Record.objects.filter(shop=s, status__exact=4).order_by('-time')
                count2 = all_list2.count()
                all_list3 = Record.objects.filter(shop=s, status__exact=2).order_by('-time')
                count3 = all_list3.count()
                all_list4 = Record.objects.filter(shop=s, status__exact=3).order_by('-time')
                count4 = all_list4.count()
                all_list5 = Record.objects.filter(shop=s, rid__startswith=today).order_by('-time')
                count5 = all_list5.count()
                all_list6 = Record.objects.filter(shop=s, time__lte=btoday).order_by('-time')
                count6 = all_list6.count()
            if request.method=="POST":
                #oper
                value = request.POST['oper']
                leng = len(value)
                ID = 0
                for i in range(1, leng):
                    ID = ID*10+int(value[i])
                r = Record.objects.get(pk=ID)
                if value[0]=='r':
                    r.status = 4
                    r.save()
                elif value[0]=='l':
                    r.status = 2
                    r.save()
                elif value[0]=='d':
                    r.status = 3
                    r.save()
                Bag_PATH = '/shops/'+str(user_id)+'/current/bag/'
                return redirect(Bag_PATH)
            return render_to_response('shops/curbag.html',
                locals(),
                context_instance=RequestContext(request)
            )

def readybag(request, user_id):
    if request.user.is_authenticated():
        user_id = request.user.id
        username = request.user.username
        is_login=True
        profile = SBProfile.objects.get(user_id=user_id)
        if profile.flag == 1:
            is_buyer = True
        else:
            is_buyer = False
        if is_buyer:
            all_list = Record.objects.filter(buyer=request.user, status__exact=1).order_by('-time')
            count1 = all_list.count()
            all_list3 = Record.objects.filter(buyer=request.user, status__exact=2).order_by('-time')
            count3 = all_list3.count()
            all_list4 = Record.objects.filter(buyer=request.user, status__exact=3).order_by('-time')
            count4 = all_list4.count()
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            all_list5 = Record.objects.filter(buyer=request.user, rid__startswith=today).order_by('-time')
            count5 = all_list5.count()
            btoday = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            all_list6 = Record.objects.filter(buyer=request.user, time__lte=btoday).order_by('-time')
            count6 = all_list6.count()
            all_list = Record.objects.filter(buyer=request.user, status__exact=4).order_by('-time')
            count2 = all_list.count()
            if request.method=="POST":
                value = request.POST['oper']
                leng = len(value)
                ID = 0
                for i in range(1, leng):
                    ID = ID*10+int(value[i])
                r = Record.objects.get(pk=ID)
                if value[0]=='l':
                    r.status = 2
                    r.save()
                Bag_PATH = '/shops/'+str(user_id)+'/ready/bag/'
                return redirect(Bag_PATH)
            return render_to_response('shops/readybag.html',
                locals(),
                context_instance=RequestContext(request)
            )
        else:
            user = request.user
            shop = user.shop_set.all()[:1]
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            btoday = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            for s in shop:
                all_list = Record.objects.filter(shop=s, status__exact=1).order_by('-time')
                count1 = all_list.count()
                all_list3 = Record.objects.filter(shop=s, status__exact=2).order_by('-time')
                count3 = all_list3.count()
                all_list4 = Record.objects.filter(shop=s, status__exact=3).order_by('-time')
                count4 = all_list4.count()
                all_list5 = Record.objects.filter(shop=s, rid__startswith=today).order_by('-time')
                count5 = all_list5.count()
                all_list6 = Record.objects.filter(shop=s, time__lte=btoday).order_by('-time')
                count6 = all_list6.count()
                all_list = Record.objects.filter(shop=s, status__exact=4).order_by('-time')
                count2 = all_list.count()
            if request.method=="POST":
                value = request.POST['oper']
                leng = len(value)
                ID = 0
                for i in range(1, leng):
                    ID = ID*10+int(value[i])
                r = Record.objects.get(pk=ID)
                if value[0]=='l':
                    r.status = 2
                    r.save()
                Bag_PATH = '/shops/'+str(user_id)+'/ready/bag/'
                return redirect(Bag_PATH)
            return render_to_response('shops/readybag.html',
                locals(),
                context_instance=RequestContext(request)
            )


def dealbag(request, user_id):
    if request.user.is_authenticated():
        user_id = request.user.id
        username = request.user.username
        is_login=True
        profile = SBProfile.objects.get(user_id=user_id)
        if profile.flag == 1:
            is_buyer = True
        else:
            is_buyer = False
        if is_buyer:
            all_list = Record.objects.filter(buyer=request.user, status__exact=1).order_by('-time')
            count1 = all_list.count()
            all_list2 = Record.objects.filter(buyer=request.user, status__exact=4).order_by('-time')
            count2 = all_list2.count()
            all_list4 = Record.objects.filter(buyer=request.user, status__exact=3).order_by('-time')
            count4 = all_list4.count()
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            all_list5 = Record.objects.filter(buyer=request.user, rid__startswith=today).order_by('-time')
            count5 = all_list5.count()
            btoday = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            all_list6 = Record.objects.filter(buyer=request.user, time__lte=btoday).order_by('-time')
            count6 = all_list6.count()
            all_list = Record.objects.filter(buyer=request.user, status__exact=2).order_by('-time')
            count3 = all_list.count()
            return render_to_response('shops/dealbag.html',
                locals(),
                context_instance=RequestContext(request)
            )
        else:
            user = request.user
            shop = user.shop_set.all()[:1]
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            btoday = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            for s in shop:
                all_list = Record.objects.filter(shop=s, status__exact=1).order_by('-time')
                count1 = all_list.count()
                all_list2 = Record.objects.filter(shop=s, status__exact=4).order_by('-time')
                count2 = all_list2.count()
                all_list4 = Record.objects.filter(shop=s, status__exact=3).order_by('-time')
                count4 = all_list4.count()
                all_list5 = Record.objects.filter(shop=s, rid__startswith=today).order_by('-time')
                count5 = all_list5.count()
                all_list6 = Record.objects.filter(shop=s, time__lte=btoday).order_by('-time')
                count6 = all_list6.count()
                all_list = Record.objects.filter(shop=s, status__exact=2).order_by('-time')
                count3 = all_list.count()
            return render_to_response('shops/dealbag.html',
                locals(),
                context_instance=RequestContext(request)
            )


def failbag(request, user_id):
    if request.user.is_authenticated():
        user_id = request.user.id
        username = request.user.username
        is_login=True
        profile = SBProfile.objects.get(user_id=user_id)
        if profile.flag == 1:
            is_buyer = True
        else:
            is_buyer = False
        if is_buyer:
            all_list = Record.objects.filter(buyer=request.user, status__exact=1).order_by('-time')
            count1 = all_list.count()
            all_list2 = Record.objects.filter(buyer=request.user, status__exact=4).order_by('-time')
            count2 = all_list2.count()
            all_list3 = Record.objects.filter(buyer=request.user, status__exact=2).order_by('-time')
            count3 = all_list3.count()
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            all_list5 = Record.objects.filter(buyer=request.user, rid__startswith=today).order_by('-time')
            count5 = all_list5.count()
            btoday = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            all_list6 = Record.objects.filter(buyer=request.user, time__lte=btoday).order_by('-time')
            count6 = all_list6.count()
            all_list = Record.objects.filter(buyer=request.user, status__exact=3).order_by('-time')
            count4 = all_list.count()
            return render_to_response('shops/failbag.html',
                locals(),
                context_instance=RequestContext(request)
            )
        else:
            user = request.user
            shop = user.shop_set.all()[:1]
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            btoday = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            for s in shop:
                all_list = Record.objects.filter(shop=s, status__exact=1).order_by('-time')
                count1 = all_list.count()
                all_list2 = Record.objects.filter(shop=s, status__exact=4).order_by('-time')
                count2 = all_list2.count()
                all_list3 = Record.objects.filter(shop=s, status__exact=2).order_by('-time')
                count3 = all_list3.count()
                all_list5 = Record.objects.filter(shop=s, rid__startswith=today).order_by('-time')
                count5 = all_list5.count()
                all_list6 = Record.objects.filter(shop=s, time__lte=btoday).order_by('-time')
                count6 = all_list6.count()
                all_list = Record.objects.filter(shop=s, status__exact=3).order_by('-time')
                count4 = all_list.count()
            return render_to_response('shops/failbag.html',
                locals(),
                context_instance=RequestContext(request)
            )

def todbag(request, user_id):
    if request.user.is_authenticated():
        user_id = request.user.id
        username = request.user.username
        is_login=True
        profile = request.user.get_profile()
        if profile.flag == 1:
            is_buyer = True
        else:
            is_buyer = False
        if is_buyer:
            # year = time.strftime('%Y', time.localtime(time.time()))
            # month = time.strftime('%m', time.localtime(time.time()))
            # day = time.strftime('%d', time.localtime(time.time()))
            # print year, month, day   
            # all_list = Record.objects.filter(buyer=request.user, time__year=year, time__month=month, year__day=day)
            # all_list = Record.objects.filter(buyer=request.user, time__contains=today)
            # all_list = Record.objects.filter(buyer=request.user, time__exact=today)
            # alist = all_list.get_count(time__year=year, time__month=month, time_day=day)
            # all_list = Record.objects.get(buyer=request.user, time__contains=today)
            # for tl in all_list:
            #     for f in tl.fooditem_set.all():
            #         print f.name, f.price, f.quantity, f.record
            # for tl in all_list:
            #     tl.time = str(tl.time)
            #     day,hour=tl.time.split()
            #     if day == today:
            #         #print day
            #         for f in tl.fooditem_set.all():
            #             print f.name, f.price, f.quantity, f.record
            all_list = Record.objects.filter(buyer=request.user, status__exact=1).order_by('-time')
            count1 = all_list.count()
            all_list2 = Record.objects.filter(buyer=request.user, status__exact=4).order_by('-time')
            count2 = all_list2.count()
            all_list3 = Record.objects.filter(buyer=request.user, status__exact=2).order_by('-time')
            count3 = all_list3.count()
            all_list4 = Record.objects.filter(buyer=request.user, status__exact=3).order_by('-time')
            count4 = all_list4.count()
            btoday = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            all_list6 = Record.objects.filter(buyer=request.user, time__lte=btoday).order_by('-time')
            count6 = all_list6.count()
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            all_list = Record.objects.filter(buyer=request.user, rid__startswith=today).order_by('-time')
            count5 = all_list.count()
            return render_to_response('shops/todbag.html',
                locals(),
                context_instance=RequestContext(request)
            )
        else:
            user = request.user
            shop = user.shop_set.all()[:1]
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            btoday = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            for s in shop:
                all_list = Record.objects.filter(shop=s, status__exact=1).order_by('-time')
                count1 = all_list.count()
                all_list2 = Record.objects.filter(shop=s, status__exact=4).order_by('-time')
                count2 = all_list2.count()
                all_list3 = Record.objects.filter(shop=s, status__exact=2).order_by('-time')
                count3 = all_list3.count()
                all_list4 = Record.objects.filter(shop=s, status__exact=3).order_by('-time')
                count4 = all_list4.count()
                all_list6 = Record.objects.filter(shop=s, time__lte=btoday).order_by('-time')
                count6 = all_list6.count()
                all_list = Record.objects.filter(shop=s, rid__startswith=today).order_by('-time')
                count5 = all_list.count()
            return render_to_response('shops/todbag.html',
                locals(),
                context_instance=RequestContext(request)
            )

def bftodbag(request, user_id):
    if request.user.is_authenticated():
        user_id = request.user.id
        username = request.user.username
        is_login=True
        profile = request.user.get_profile()
        if profile.flag == 1:
            is_buyer = True
        else:
            is_buyer = False
        if is_buyer:
            all_list = Record.objects.filter(buyer=request.user, status__exact=1).order_by('-time')
            count1 = all_list.count()
            all_list2 = Record.objects.filter(buyer=request.user, status__exact=4).order_by('-time')
            count2 = all_list2.count()
            all_list3 = Record.objects.filter(buyer=request.user, status__exact=2).order_by('-time')
            count3 = all_list3.count()
            all_list4 = Record.objects.filter(buyer=request.user, status__exact=3).order_by('-time')
            count4 = all_list4.count()
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            all_list5 = Record.objects.filter(buyer=request.user, rid__startswith=today).order_by('-time')
            count5 = all_list5.count()
            btoday = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            all_list = Record.objects.filter(buyer=request.user, time__lte=btoday).order_by('-time')
            count6 = all_list.count()
            return render_to_response('shops/bftodbag.html',
                locals(),
                context_instance=RequestContext(request)
            )
        else:
            user = request.user
            shop = user.shop_set.all()[:1]
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            btoday = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            for s in shop:
                all_list = Record.objects.filter(shop=s, status__exact=1).order_by('-time')
                count1 = all_list.count()
                all_list2 = Record.objects.filter(shop=s, status__exact=4).order_by('-time')
                count2 = all_list2.count()
                all_list3 = Record.objects.filter(shop=s, status__exact=2).order_by('-time')
                count3 = all_list3.count()
                all_list4 = Record.objects.filter(shop=s, status__exact=3).order_by('-time')
                count4 = all_list4.count()
                all_list5 = Record.objects.filter(shop=s, rid__startswith=today).order_by('-time')
                count5 = all_list5.count()
                all_list = Record.objects.filter(shop=s, time__lte=btoday).order_by('-time')
                count6 = all_list.count()
            return render_to_response('shops/bftodbag.html',
                locals(),
                context_instance=RequestContext(request)
            )
def allfood(request, user_id):
    if request.user.is_authenticated():
        user_id = request.user.id
        username = request.user.username
        is_login=True
        profile = request.user.get_profile()
        if profile.flag == 1:
            is_buyer = True
        else:
            is_buyer = False
        shop = request.user.shop_set.all()
        for s in shop:
            food_list = s.food_set.all()
        if request.method=="POST":
            value = request.POST['oper']
            leng = len(value)
            food_id = 0
            for i in range(1, leng):
                food_id = food_id*10+int(value[i])
            if value[0]=="d":
                for s in shop:
                    s.food_set.filter(pk=food_id).delete()
            if value[0]=="m":
                for s in shop:
                    mf = s.food_set.get(pk=food_id)
                MDF_PATH='/shops/'+str(user_id)+'/mdf/'+str(food_id)+'/food/'
                return redirect(MDF_PATH)
    return render_to_response('shops/allfood.html',
        locals(),
        context_instance=RequestContext(request)
    )

def addfood(request, user_id):
    if request.user.is_authenticated():
        user_id = request.user.id
        username = request.user.username
        is_login=True
        profile = request.user.get_profile()
        if profile.flag == 1:
            is_buyer = True
        else:
            is_buyer = False
        if request.method=='POST':
            form = AddFoodForm(request.POST)
            if form.is_valid():
                name = request.POST['name']
                price = request.POST['price']
                shop = request.user.shop_set.all()
                for s in shop:
                    food = Food(name=name, price=price, shop=s)
                    food.save()
                ALL_PATH = '/shops/'+str(user_id)+'/all/food/'
                return redirect(ALL_PATH)
        else:
            form = AddFoodForm()
    return render_to_response('shops/addfood.html',
        locals(),
        context_instance=RequestContext(request)
    )

def mdffood(request, user_id, food_id):
    if request.user.is_authenticated():
        user_id = request.user.id
        username = request.user.username
        is_login=True
        profile = request.user.get_profile()
        if profile.flag == 1:
            is_buyer = True
        else:
            is_buyer = False
        shop = request.user.shop_set.all()
        for s in shop:
            mf = s.food_set.get(pk=food_id)
        if request.method=="POST":
            name = request.POST['fname']
            price =  request.POST['fprice']
            for s in shop:
                s.food_set.filter(pk=food_id).update(name=name, price=price)
            ALL_PATH = '/shops/'+str(user_id)+'/all/food/'
            return redirect(ALL_PATH)
    return render_to_response('shops/mdffood.html',
        locals(),
        context_instance=RequestContext(request)
    )
