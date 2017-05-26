from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, Http404, HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from .forms import *
from .models import *
from django.utils import timezone
from django.template import RequestContext

# Create your views here.

#首页
def welcome(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        lf = LoginForm(request.POST)
        if lf.is_valid():
            _Username = lf.cleaned_data['username']
            _Password = lf.cleaned_data['password']
            user = auth.authenticate(username=_Username, password=_Password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('home')
            else:
                return HttpResponse(u"用户或密码错误")
    else:
        lf = LoginForm()
    return render(request,'welcome.html', { 'lf':lf, })

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        rf = RegistForm(request.POST)

        if rf.is_valid():
            _Username = request.POST.get('username')
            _Email = request.POST.get('email')
            _Password = request.POST.get('password')
            _Password2 = request.POST.get('passwordagain')
            _College = request.POST.get('college')
            _Major = request.POST.get('major')
            _IDnum = request.POST.get('IDnum')
            _Name = request.POST.get('name')
            _Grade = request.POST.get('grade')
            _Sex = request.POST.get('sex')

            if _Password != _Password2:
                return HttpResponse(u"两次密码不一致")
            filterResult = User.objects.filter(username=_Username)  # c************
            if len(filterResult) > 0:
                return HttpResponse("用户名已存在")

            user = User.objects._create_user(username=_Username, password=_Password, email=_Email, )
            account = Account()
            account.user_id = user.id
            account.college = _College
            account.major = _Major
            account.IDnum = _IDnum
            account.realname = _Name
            account.grade = _Grade
            account.sex = _Sex
            account.save()
            auth.login(request, user)
            return redirect('home')
    else:
        rf = RegistForm()
    return render(request,'register.html', {'rf': rf, })

#主页的部分
@login_required(login_url='/')
def home(request):
    user = request.user
    membership = Account_Community.objects.filter(account=user)
    normal_blog = Blog.objects.filter(type=1)
    notice_blog = Blog.objects.filter(type=2)
    twit = Twit.objects.all()
    response = render_to_response('home.html', {'user': user, 'memberships': membership, 'normal_blogs':normal_blog,
                                                "notice_blogs": notice_blog, 'twits': twit})
    response.set_cookie('username', user, 3600)
    return response

@login_required(login_url="/")
def logout(request):
    auth.logout(request)
    respon = redirect('/')
    respon.delete_cookie('username')
    respon.delete_cookie('member')
    return respon

@login_required(login_url="/")
def selfinfo(request):
    user = request.user
    membership = Account_Community.objects.filter(account=user)
    profile = user.account
    return render(request, 'selfinfo.html', {'user':user, 'profile':profile, 'memberships': membership})

@login_required(login_url="/")
def get_user(request):
    user = request.user
    membership = Account_Community.objects.filter(account=user)
    userlist = User.objects.all()
    dic = {'userlist': userlist, 'memberships': membership}
    # watch userlist, which is made of name and its info
    return render(request, 'user.html', dic)

@login_required(login_url="/")
def get_activity(request):
    user = request.user
    membership = Account_Community.objects.filter(account=user)
    dic = {}
    atys = Activity.objects.all()
    dic['activities'] = atys
    dic['memberships'] = membership
    return render(request, '_activity.html', dic)

@login_required(login_url="/")
def get_community(request):
    dic = {}
    user = request.user
    membership = Account_Community.objects.filter(account=user)
    cmts = Community.objects.all()
    dic['communities'] = cmts
    dic['memberships'] = membership
    return render(request, '_community.html', dic)

@login_required(login_url="/")
def get_message(request):
    user = request.user
    dic = {}
    membership = Account_Community.objects.filter(account=user)
    # 我发出的inform和我收到的inform
    if user:
        get_informs = Private_Message.objects.filter(acceptor=user)
        send_informs = Private_Message.objects.filter(sender=user)
        dic['gets'] = get_informs
        dic['sends'] = send_informs
        return render(request, '_message.html', dic)
    return HttpResponse('Error')

#社团的部分
def Communityhomepage(request, Community_name):
    user = request.user
    membership = Account_Community.objects.filter(account=user)
    Invalid_Input = request.GET.get('Invalid_Input')
    try:
        _community = Community.objects.get(name=str(Community_name))
        # _Cabinet = Cabinet.objects.filter(Room_address=Room.Room_name)
    except Community.DoesNotExist:
        raise Http404
    return render(request,'homepage.html', {'community': _community, 'Invaild_Input': Invalid_Input,
                                            'memberships': membership})

@login_required(login_url="/")
def Community_console(request, Community_name):
    user = request.user
    membership = Account_Community.objects.filter(account=user)
    Invalid_Input = request.GET.get('Invalid_Input')
    try:
        _community = Community.objects.get(name=str(Community_name))
        #_Cabinet = Cabinet.objects.filter(Room_address=Room.Room_name)
    except Community.DoesNotExist:
        raise Http404
    return render(request,'console.html', {'community': _community, 'Invaild_Input': Invalid_Input,
                                           'memberships': membership})

@login_required(login_url="/")
def Community_activity(request, Community_name):
    user = request.user
    membership = Account_Community.objects.filter(account=user)
    Invalid_Input = request.GET.get('Invalid_Input')
    try:
        _community = Community.objects.get(name=str(Community_name))
        _activity = Activity.objects.filter(community=Community_name)
        #_Cabinet = Cabinet.objects.filter(Room_address=Room.Room_name)
    except Community.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        af = Create_activityForm(request.POST)
        if af.is_valid():
            _name=request.POST.get('name')
            _datetime=request.POST.get('datetime')
            _address=request.POST.get('address')
            _introduction=request.POST.get('introduction')
            Activity.objects.create(community=_community, name=_name, datetime=_datetime, address=_address,
                                    introduction=_introduction)
            _activity = Activity.objects.filter(community=Community_name)
    else:
        af = Create_activityForm()
    return render(request,'console_activity.html', {'community': _community, 'Invaild_Input': Invalid_Input,
                                                    'activities': _activity, 'af': af, 'memberships':membership})

@login_required(login_url="/")
def Community_member(request, Community_name):
    user = request.user
    membership = Account_Community.objects.filter(account=user)
    Invalid_Input = request.GET.get('Invalid_Input')
    try:
        _community = Community.objects.get(name=str(Community_name))
        _member = Account_Community.objects.filter(community=Community_name)
        #_Cabinet = Cabinet.objects.filter(Room_address=Room.Room_name)
    except Community.DoesNotExist:
        raise Http404
    return render(request,'console_member.html', {'community': _community, 'Invaild_Input': Invalid_Input,
                                                  'members': _member, 'memberships': membership})

@login_required(login_url="/")
def Community_blog(request, Community_name):
    user = request.user
    membership = Account_Community.objects.filter(account=user)
    Invalid_Input = request.GET.get('Invalid_Input')
    try:
        _community = Community.objects.get(name=str(Community_name))
        _blog = Blog.objects.filter(author=Community_name)
    except Community.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        bf = Create_blogForm(request.POST)
        if bf.is_valid():
            _title = request.POST.get('title')
            _type = request.POST.get('type')
            _excerpt = request.POST.get('excerpt')
            _body = request.POST.get('body')
            Blog.objects.create(author=_community, title=_title,  body=_body, type=_type, excerpt=_excerpt)
            _blog = Blog.objects.filter(author=Community_name)
    else:
        bf = Create_blogForm()
    return render(request, 'console_blog.html', {'community': _community, 'Invaild_Input': Invalid_Input,
                                                 'blogs': _blog, 'bf': bf, 'memberships': membership})

@login_required(login_url="/")
def Community_twit(request, Community_name):
    user = request.user
    membership = Account_Community.objects.filter(account=user)
    Invalid_Input = request.GET.get('Invalid_Input')
    try:
        _community = Community.objects.get(name=str(Community_name))
        _twit = Twit.objects.filter(author=Community_name)
    except Community.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        tf = Create_twitForm(request.POST)
        if tf.is_valid():
            _content = request.POST.get('content')
            Twit.objects.create(author=_community, content=_content,)
            _twit = Twit.objects.filter(author=Community_name)
    else:
        tf = Create_twitForm()
    return render(request, 'console_twit.html', {'community': _community, 'Invaild_Input': Invalid_Input,
                                                 'twits': _twit, 'tf': tf, 'memberships': membership})

#租户部分
def Tenant_welcome(request):
    return render(request, 'tenant_welcome.html')

def Tenant_home(request, Community_name):
    Invalid_Input = request.GET.get('Invalid_Input')
    try:
        _community = Community.objects.get(name=str(Community_name))
    except Community.DoesNotExist:
        raise Http404
    return render(request, 'tenant_home.html',{'community': _community})

def Tenant_feature(request, Community_name):
    Invalid_Input = request.GET.get('Invalid_Input')
    try:
        _community = Community.objects.get(name=str(Community_name))
    except Community.DoesNotExist:
        raise Http404
    Table = MT_Tables.objects.filter(Tenant=Community_name)
    Col = MT_Fields.objects.filter(Tenant=Community_name)
    Value = MT_Data.objects.filter(Tenant=Community_name)
    return render(request, 'tenant_featureCus.html',{'community': _community, 'Tables': Table, 'Cols': Col,
                                                     'Values': Value})