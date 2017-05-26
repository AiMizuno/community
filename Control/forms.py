from django import forms
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(label=u'账号', required=True, max_length=30)
    password = forms.CharField(label=u'密码',required=True,widget=forms.PasswordInput(), max_length=20)


#注册
college_choice = (
    ('SDCS', u"数据科学与计算机学院"),
    ('ABC', u"电信学院"),
    ('BS', u"管理学院"),
)

sex_choice = (
    (1, u'男'),
    (2, u'女'),
)

class RegistForm(forms.Form):
    username = forms.CharField(label=u"账号", required=True,)
    password = forms.CharField(label=u"密码", required=True, widget=forms.PasswordInput())
    passwordagain = forms.CharField(label=u"确认密码", required=True, widget=forms.PasswordInput())
    sex = forms.ChoiceField(label=u'性别', required=True, choices=sex_choice)
    email = forms.EmailField(label=u'邮箱', required=True)
    name = forms.CharField(label=u'真实姓名', required=True)
    IDnum = forms.IntegerField(label=u'学号', required=True)
    grade = forms.IntegerField(label=u'年级', required=True)
    major = forms.CharField(label=u'专业', required=True)
    college = forms.ChoiceField(label=u"学院", required=True, choices=college_choice)

class Create_activityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'datetime', 'address', 'introduction']

class Create_blogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'type', 'excerpt', 'body']

class Create_twitForm(forms.ModelForm):
    class Meta:
        model = Twit
        fields = ['content']