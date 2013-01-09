from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from users.models import SBProfile
from users.forms import LoginForm, RegisterForm, MdfinfoForm, MdfpwdForm

##########################################################################
#User Login in and Logout########################################################
##########################################################################
def home(request):
    username=''
    if request.user.is_authenticated():
        is_login = True
        user_id = request.user.id
        username = request.user.username
        profile = request.user.get_profile()
        if profile.flag == 1:
            is_buyer = True
        else:
            is_buyer = False
        return render_to_response('home.html',
        locals(),
        context_instance=RequestContext(request)
    )
    else:
        is_login = False
    return render_to_response('home.html',
        locals(),
        context_instance=RequestContext(request)
    )

def sblogin(request):
    username=''
    errors_msg=[]
    if request.user.is_authenticated():
        is_login = True
        user_id = request.user.id
        username = request.user.username
        profile = request.user.get_profile()
        if profile.flag == 1:
            is_buyer = True
        else:
            is_buyer = False
        errors_msg.append('You have already logged in!')
        return render_to_response('home.html',
            locals(),
            context_instance=RequestContext(request)
        )
    else:
        is_login = False
        if request.method=="POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('users.views.home')
                    else:
                        errors_msg.append('Your account had been disabled!')
                        return render_to_response('home.html',
                            locals(),
                            context_instance=RequestContext(request)
                        )
                else:
                    errors_msg.append('Username and password do not match!')
        else:
            form = LoginForm()
        return render_to_response('users/login.html',
            locals(),
            context_instance=RequestContext(request)
        )

def sblogout(request):
    logout(request)
    is_login = False
    return render_to_response('home.html',
        locals(),
        context_instance=RequestContext(request)
    )

def sbregister(request):
    errors_msg = []
    if request.method=="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            rptpwd = request.POST['rptpwd']
            sbid = request.POST['idnum']
            name = request.POST['name']
            teleph = request.POST['teleph']
            address = request.POST['address']
            user = User.objects.create_user(username=username, password=password)
            user.save()
            profile = SBProfile(user=user, sbid=sbid, name=name, teleph=teleph, address=address, flag=1)
            profile.save()
            #login the user in
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('users.views.home')
        else:
            errors_msg.append('Input invalid!')
    else:
        form = RegisterForm()
    return render_to_response('users/register.html',
        locals(),
        context_instance=RequestContext(request)
    )

############################################################################
#After Log in###################################################################
############################################################################
def myinfo(request, user_id): #######get from mysql
    errors_msg = []
    if request.user.is_authenticated():
        user_id = request.user.id
        username = request.user.username
        is_login = True
	profile = request.user.get_profile()
        if profile.flag == 1:
            is_buyer = True
        else:
            is_buyer = False
        #look it
        try:
	    profile = request.user.get_profile()
        except:
            errors_msg.append('You have not fill your info, so you can not see anything!')
            return render_to_response('home.html',
                locals(),
                context_instance=RequestContext(request)
            )
        else:
            idnum = profile.sbid
            name = profile.name
            teleph = profile.teleph
            address = profile.address
            return render_to_response('users/info.html',
                locals(),
                context_instance = RequestContext(request)
            )
    else:
        errors_msg.append('You have not logged in, so you can not see anything!')
        return render_to_response('home.html',
            locals(),
            context_instance=RequestContext(request)
        )

def mdfinfo(request, user_id):################modify to mysql
    errors_msg = []
    success_msg = []
    mdf = False
    if request.user.is_authenticated():
        user_id = request.user.id
        username = request.user.username
        is_login = True
        profile = request.user.get_profile()
        if profile.flag == 1:
            is_buyer = True
        else:
            is_buyer = False
        if request.method=="POST":
            form = MdfinfoForm(request.POST)
            if form.is_valid():
                idnum = request.POST['idnum']
                name = request.POST['name']
                teleph = request.POST['teleph']
                address = request.POST['address']
                #modify it
                profile = request.user.get_profile()
                if idnum:
                    profile.sbid = idnum
                    mdf = True
                if name:
                    profile.name = name
                    mdf = True
                if teleph:
                    profile.teleph = teleph
                    mdf = True
                if address:
                    profile.address = address
                    mdf = True
                if mdf:
                    profile.save()
                    success_msg.append('Modify successfully!')
                else:
                    success_msg.append('Nothing Changed!')
                return render_to_response('users/mdfinfo.html',
                    locals(),
                    context_instance = RequestContext(request)
                )
        else:
            form = MdfinfoForm()
        return render_to_response('users/mdfinfo.html',
            locals(),
            context_instance = RequestContext(request)
        )
    else:
        errors_msg.append('You have not logged in, so you can not modify anything!')
        return render_to_response('home.html',
            {'errors_msg':errors_msg,
            },
            context_instance=RequestContext(request)
        )

def mdfpwd(request, user_id):
    errors_msg = []
    success_msg=[]
    if request.user.is_authenticated():
        user_id = request.user.id
        username = request.user.username
        is_login = True
        profile = request.user.get_profile()
        if profile.flag == 1:
            is_buyer = True
        else:
            is_buyer = False
        if request.method=="POST":
            form = MdfpwdForm(request.POST)
            if form.is_valid():
                oldpwd = request.POST['oldpwd']
                user = User.objects.get(id=user_id)
                if user.check_password(oldpwd):
                    newpwd = request.POST['newpwd']
                    user.set_password(newpwd)
                    user.save()
                    success_msg.append('Modify successfully!')
                    return render_to_response('users/mdfpwd.html',
                        locals(),
                        context_instance = RequestContext(request)
                    )
                else:
                    errors_msg.append('Wrong password!')
                    return render_to_response('users/mdfpwd.html',
                        locals(),
                        context_instance=RequestContext(request)
                        )
        else:
            form = MdfpwdForm()
        return render_to_response('users/mdfpwd.html',
            locals(),
            context_instance = RequestContext(request)
        )
    else:
        errors_msg.append('You have not logged in, so you can not modify anything!')
        return render_to_response('home.html',
            locals(),
            context_instance=RequestContext(request)
        )
